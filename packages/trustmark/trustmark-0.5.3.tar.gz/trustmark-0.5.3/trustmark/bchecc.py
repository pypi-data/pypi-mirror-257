from dataclasses import dataclass
from copy import deepcopy


class BCH(object):

   @dataclass
   class BCHcontrol:
      m: int
      t: int
      poly: int

   @dataclass
   class GFpoly:
      deg: int



   def ecc_words(self):
      return self.DIV_ROUND_UP(self.BCHstruct.m*self.BCHstruct.t, 32)

   def ecc_bytes(self):
      return self.DIV_ROUND_UP(self.BCHstruct.m * self.BCHstruct.t, 8)

   def DIV_ROUND_UP(self, a, b):
      return  int((a + b - 1) / b)

   ### GALOIS

   def gf_poly_logrep(self, a):
    rep=[0]*(self.BCHstruct.t*2)
    d=a.deg
    l=self.BCHstruct.n-self.a_log(a.c[a.deg])
    for i in range(0,d):
       if a.c[i]:
         rep[i]=self.mod(self.a_log(a.c[i])+l)
       else:
         rep[i]=-1
    return rep


   def gf_inv(self,a):
      return self.BCHstruct.a_pow_tab[self.BCHstruct.n - self.BCHstruct.a_log_tab[a]]    

   def gf_sqr(self, a):
      if a:
         return self.BCHstruct.a_pow_tab[self.mod(2*self.BCHstruct.a_log_tab[a])]
      else:
         return 0

   def mod(self, v):
       if v<self.BCHstruct.n:
         return v
       else:
         return v-self.BCHstruct.n

   def gf_mul(self, a,b):

      if (a>0 and b>0):
        res=self.mod(self.BCHstruct.a_log_tab[a]+self.BCHstruct.a_log_tab[b])
        return (self.BCHstruct.a_pow_tab[res])
      else:
        return 0

   def gf_div(self,a,b):
      if a:
        return self.BCHstruct.a_pow_tab[self.mod(self.BCHstruct.a_log_tab[a]+self.BCHstruct.n-self.BCHstruct.a_log_tab[b])]
      else:
        return 0

   def modulo(self, v):
      n=self.BCHstruct.n
      while (v>=n):
         v -= n
         v = (v & n) + (v >> self.BCHstruct.m)
      return v

   def a_log(self, x):
      return self.BCHstruct.a_log_tab[x]

   def a_ilog(self, x):
      return self.mod(self.BCHstruct.n- self.BCHstruct.a_log_tab[x])

   def a_pow(self, i):
      return self.BCHstruct.a_pow_tab[self.modulo(i)]

   def deg(self, x):
      count=0
      while (x >> 1):
          x = x >> 1
          count += 1
      return count

   

   def load4bytes(self, data):
      w=0
      w += data[0] << 24
      w += data[1] << 16
      w += data[2] << 8
      w += data[3] << 0
      return w


   def find_poly_roots(self, k, poly):

      roots=[]
      
      if poly.deg>4: 
         k=k*8+self.BCHstruct.ecc_bits
         rep=self.gf_poly_logrep(poly)
         rep[poly.deg]=0
         syn0=self.gf_div(poly.c[0],poly.c[poly.deg])
         for i in range(self.BCHstruct.n-k+1, self.BCHstruct.n+1):
             syn=syn0
             for j in range(1,poly.deg+1):
                 m=rep[j]
                 if m>=0:
                    syn = syn ^ self.a_pow(m+j*i)
             if syn==0:
                 roots.append(self.BCHstruct.n-i)
                 if len(roots)==poly.deg:
                     break


      if poly.deg==1:
         if (poly.c[0]):
            roots.append(self.mod(self.BCHstruct.n-self.BCHstruct.a_log_tab[poly.c[0]]+self.BCHstruct.a_log_tab[poly.c[1]]) )

      if poly.deg==2:
         if (poly.c[0] and poly.c[1]):
            l0=self.BCHstruct.a_log_tab[poly.c[0]]        
            l1=self.BCHstruct.a_log_tab[poly.c[1]]        
            l2=self.BCHstruct.a_log_tab[poly.c[2]]        

            u=self.a_pow(l0+l2+2*(self.BCHstruct.n-l1))
            r=0
            v=u
            while (v):
               i=self.deg(v)
               r = r ^ self.BCHstruct.xi_tab[i]
               v = v ^ pow(2,i)
            if self.gf_sqr(r)^r == u:
               roots.append(self.modulo(2*self.BCHstruct.n-l1-self.BCHstruct.a_log_tab[r]+l2))
               roots.append(self.modulo(2*self.BCHstruct.n-l1-self.BCHstruct.a_log_tab[r^1]+l2))

      if poly.deg==3:
            if poly.c[0]:
               e3=poly.c[3]
               c2=self.gf_div(poly.c[0],e3)
               b2=self.gf_div(poly.c[1],e3)
               a2=self.gf_div(poly.c[2],e3)

               c=self.gf_mul(a2,c2)
               b=self.gf_mul(a2,b2)^c2
               a=self.gf_sqr(a2)^b2

               tmp=self.find_affine4_roots(a,b,c)
               if len(tmp)==4:
                  for i in range(0,4):
                     if tmp[i]!=a2:
                       roots.append(self.a_ilog(tmp[i]))
               else:
                  self.BCHstruct.errloc=[]
                  return -1

      if poly.deg==4:
            if poly.c[0]:
              e4=poly.c[4]
              e=0
              d=self.gf_div(poly.c[0],e4)
              c=self.gf_div(poly.c[1],e4)
              b=self.gf_div(poly.c[2],e4)
              a=self.gf_div(poly.c[3],e4)
              if a:
                if c:
                   f=self.gf_div(c,a)
                   l=self.a_log(f)
                   if l & 1:
                      l+=self.BCHstruct.n
                   e=self.a_pow(int(l/2))
                   d=self.a_pow(2*l) ^ self.gf_mul(b,f)^d
                   b=self.gf_mul(a,e)^b
                if d==0:   
                   self.BCHstruct.errloc=[]                 
                   return 0
                c2=self.gf_inv(d)
                b2=self.gf_div(a,d)
                a2=self.gf_div(b,d)
              else:
                c2=d
                b2=c
                a2=b
              rts=self.find_affine4_roots(a2,b2,c2)
            n=0
            if len(rts)==4:
              for i in range(0,4):
               if a:
                 f=self.gf_inv(rts[i])
               else:
                 f=rts[i]
               rts[i]= self.a_ilog(f^e)
               roots=rts



      self.BCHstruct.errloc=roots  
      return len(roots)

   def get_ecc_bits(self):
      return self.BCHstruct.ecc_bits


   def get_ecc_bytes(self):
      return self.BCHstruct.ecc_bytes


   def compute_syndrome(self, eccbuf):

      s=self.BCHstruct.ecc_bits
      t=self.BCHstruct.t
      syn=[0]*(2*t)

      m= s & 31

      if (m):
        eccbuf[int(s/32)] = eccbuf[int(s/32)] & ~(pow(2,32-m)-1)

      eccptr=0
      while(s>0 or eccptr==0):
          poly=eccbuf[eccptr]
          eccptr += 1
          s-= 32
          while (poly):
             i=self.deg(poly)
             for j in range(0,(2*t),2):
               syn[j]=syn[j] ^ self.a_pow((j+1)*(i+s))
             poly = poly ^ pow(2,i)


      for i in range(0,t):
         syn[2*i+1]=self.gf_sqr(syn[i])


      return syn

   def find_affine4_roots(self,a,b,c):
      m=self.BCHstruct.m
      mask=0xffff
      j=self.a_log(b)
      k=self.a_log(a)
      rows=[0]*32
      rows[0]=c

      for i in range(0,m):
         if a:
             at=self.BCHstruct.a_pow_tab[self.mod(k)]
         else:
             at=0
         if b:
             bt=self.BCHstruct.a_pow_tab[self.mod(j)]
         else:
             bt=0
         rows[i+1]=self.BCHstruct.a_pow_tab[4*i]^ at ^ bt
         j+=1
         k+=2


      j=16
      while (j!=0):
          k=0
          while (k<16):
            t=((rows[k] >> j)^rows[k+j]) & mask
            rows[k] = rows[k] ^ (t << j)
            rows[k+j] ^= t
            k=(j+k+1) & ~j
          j = j >> 1
          mask = mask ^ (mask << j)


      return self.solve_linear_system(rows,4)


   def solve_linear_system(self,rows,nsol):


       m=self.BCHstruct.m
       param=[0]* 31

       k=0
       mask = pow(2,m)

       for c in range(0,m):
           rem=0
           p=c-k
           for r in range(p,m):
               if (rows[r] & mask):
                 if (r != p) :
                   tmp=rows[r]
                   rows[r]=rows[p]
                   rows[p]=tmp
                 rem = r+1
                 break

           if (rem):
              tmp=rows[p]
              for r in range(rem,m):
                 if rows[r] & mask:
                    rows[r] = rows[r] ^ tmp

           else:
              param[k]=c
              k+=1
           mask = mask >> 1

       if k>0:
          p=k
          for r in range(m-1, -1, -1):
             if ((r > m-1-k) and rows[r]):
                return []
             if (p and (r == param[p-1])):
                p=p-1
                rows[r]=pow(2,m-r)
             else:
                rows[r]=rows[r-p]

       if nsol != pow(2,k):
          return []

       sol=[0]*nsol
       for p in range(0,nsol):
          for c in range(0,k):
               rows[param[c]] = (rows[param[c]] & ~1) | ((p>>c)&1)

          tmp=0
          for r in range(m-1,-1,-1):
               mask = rows[r] & (tmp | 1)
               parmask=mask ^ (mask >> 1)
               parmask=parmask ^ (parmask >> 2)
               parmask = (parmask & 0x11111111) * 0x11111111
               parmask = (parmask >> 28 ) & 1
               tmp = tmp | parmask << (m-r)
          sol[p]=tmp>>1

       return sol




   def compute_error_locator_polynomial(self, syn):

       n=self.BCHstruct.n
       t=self.BCHstruct.t
       pp=-1
       pd=1

       pelp=self.GFpoly(deg=0)
       pelp.deg=0
       pelp.c= [0]*(2*t)
       pelp.c[0]=1

       elp=self.GFpoly(deg=0)
       elp.c= [0]*(2*t)
       elp.c[0]=1

       d=syn[0]

       elp_copy=self.GFpoly(deg=0)
       for i in range(0,t):
          if (elp.deg>t):
              break
          if d:
             k=2*i-pp
             elp_copy=deepcopy(elp)
             tmp=self.a_log(d)+n-self.a_log(pd)
             for j in range(0,(pelp.deg+1)):
               if (pelp.c[j]):
                 l=self.a_log(pelp.c[j])
                 elp.c[j+k]=elp.c[j+k] ^ self.a_pow(tmp+l)

             tmp=pelp.deg+k
             if tmp>elp.deg:
                 elp.deg=tmp
                 pelp=deepcopy(elp_copy)
                 pd=d
                 pp=2*i
          if (i<t-1):
              d=syn[2*i+2]
              for j in range(1,(elp.deg+1)):
                  d = d ^ self.gf_mul(elp.c[j],syn[2*i+2-j])


       self.BCHstruct.elp=elp

       return elp.deg    



   def decode(self,data,recvecc):

      calc_ecc=self.encode(data)

      self.BCHstruct.errloc=[]

      ecclen=len(recvecc)
      mlen=int(ecclen/4) # how many whole words
      eccbuf=[]
      offset=0
      while (mlen>0):
         w=self.load4bytes(recvecc[offset:(offset+4)])
         eccbuf.append(w)
         offset+=4
         mlen -=1
      recvecc=recvecc[offset:]
      leftdata=len(recvecc)
      if leftdata>0: #pad it to 4
        recvecc=recvecc+bytes([0]*(4-leftdata))
        w=self.load4bytes(recvecc)
        eccbuf.append(w)

      eccwords=self.ecc_words()
      sum=0
      for i in range(0,eccwords):
         self.BCHstruct.ecc_buf[i] = self.BCHstruct.ecc_buf[i] ^ eccbuf[i]
         sum = sum | self.BCHstruct.ecc_buf[i]
      if sum==0:
        return 0 # no bit flips

      syn=self.compute_syndrome(self.BCHstruct.ecc_buf)

      self.compute_error_locator_polynomial(syn)

      nroots = self.find_poly_roots(len(data),self.BCHstruct.elp)
      datalen=len(data)
      nbits=(datalen*8)+self.BCHstruct.ecc_bits

      for i in range(0,nroots):
          if self.BCHstruct.errloc[i] >= nbits:
            return -1
          self.BCHstruct.errloc[i]=nbits-1-self.BCHstruct.errloc[i]
          self.BCHstruct.errloc[i]=(self.BCHstruct.errloc[i] & ~7) | (7-(self.BCHstruct.errloc[i] & 7))
        

      for bitflip in self.BCHstruct.errloc:
          byte= int (bitflip / 8)
          bit = pow(2,(bitflip & 7))
          if bitflip < (len(data)+len(recvecc))*8:
            if byte<len(data):
              data[byte] = data[byte] ^ bit
            else:
              recvecc[byte - len(data)] = recvecc[byte - len(data)] ^ bit


      return nroots


   def encode(self,data):

      datalen=len(data)
      l=self.ecc_words()-1
      ecc= [0]*self.BCHstruct.ecc_bytes

      ecc_max_words=self.DIV_ROUND_UP(31*64, 32)
      r = [0]*ecc_max_words

      tab0idx=0
      tab1idx=tab0idx+256*(l+1)
      tab2idx=tab1idx+256*(l+1)
      tab3idx=tab2idx+256*(l+1)
  
      mlen=int(datalen/4) # how many whole words
      offset=0
      while (mlen>0):
         w=self.load4bytes(data[offset:(offset+4)])
         w=w^r[0]
         p0=tab0idx+(l+1)*((w>>0) & 0xff)
         p1=tab1idx+(l+1)*((w>>8) & 0xff)
         p2=tab2idx+(l+1)*((w>>16) & 0xff)
         p3=tab3idx+(l+1)*((w>>24) & 0xff)
      
         for i in range(0,l):
           r[i]=r[i+1] ^ self.BCHstruct.mod8_tab[p0+i] ^ self.BCHstruct.mod8_tab[p1+i] ^ self.BCHstruct.mod8_tab[p2+i] ^ self.BCHstruct.mod8_tab[p3+i]

         r[l] = self.BCHstruct.mod8_tab[p0+l]^self.BCHstruct.mod8_tab[p1+l]^self.BCHstruct.mod8_tab[p2+l]^self.BCHstruct.mod8_tab[p3+l];
         mlen -=1
         offset +=4


      data=data[offset:]
      leftdata=len(data)
      
      ecc=r
      posn=0
      while (leftdata):
          tmp=data[posn]
          posn += 1
          pidx = (l+1)*(((ecc[0] >> 24)^(tmp)) & 0xff)
          for i in range(0,l):
             ecc[i]=(((ecc[i] << 8)&0xffffffff)|ecc[i+1]>>24)^(self.BCHstruct.mod8_tab[pidx])
             pidx += 1
          ecc[l]=((ecc[l] << 8)&0xffffffff)^(self.BCHstruct.mod8_tab[pidx])
          leftdata -= 1

      self.BCHstruct.ecc_buf=ecc
      eccout=[]
      for e in r:
         e1=(e >> 24) & 0xff
         e2=(e >> 16) & 0xff
         e3=(e >> 8) & 0xff
         e4=(e >> 0) & 0xff
         eccout.append(e1)
         eccout.append(e2)
         eccout.append(e3)
         eccout.append(e4)

      eccout=eccout[0:self.BCHstruct.ecc_bytes]

      eccbytes=(bytearray(bytes(eccout)))
      return eccbytes



   def build_mod8_tables(self, g):

     l=self.ecc_words()
     plen=self.DIV_ROUND_UP(self.BCHstruct.ecc_bits+1,32)
     ecclen=self.DIV_ROUND_UP(self.BCHstruct.ecc_bits,32)

     self.BCHstruct.mod8_tab = [0] * 4*256*l
   
     for i in range(0,256):
        for b in range(0,4):
          offset= (b*256+i)*l
          data = i << 8*b
          while (data):

            d=self.deg(data)
            data = data ^ (g[0] >> (31-d))
            for j in range(0,ecclen):
               if d<31:
                 hi=(g[j] << (d+1)) & 0xffffffff
               else:
                 hi=0
               if j+1 < plen:
                 lo= g[j+1] >> (31-d)
               else:
                 lo= 0
               self.BCHstruct.mod8_tab[j+offset] = self.BCHstruct.mod8_tab[j+offset] ^ (hi | lo)


   def __init__(self, t, poly):

      tmp = poly;
      m = 0;
      while (tmp >> 1):
         tmp =tmp >> 1 
         m +=1  
 
      self.BCHstruct=self.BCHcontrol(m=m,t=t,poly=poly)

      self.BCHstruct.n=pow(2,m)-1
      words = self.DIV_ROUND_UP(m*t,32)
      self.BCHstruct.ecc_bytes = self.DIV_ROUND_UP(m*t,8)
      self.BCHstruct.a_pow_tab=[0]*(1+self.BCHstruct.n)
      self.BCHstruct.a_log_tab=[0]*(1+self.BCHstruct.n)
      self.BCHstruct.xi_tab=[0]*(1+self.BCHstruct.m)
      self.BCHstruct.mod8_tab=[0]*(words*1024)
      self.BCHstruct.syn=[0]*(2*t)
      self.BCHstruct.elp=[0]*(t+1)
      self.BCHstruct.errloc=[0] * t
 

      x=1
      k=pow(2,self.deg(poly))
      if k != pow(2,self.BCHstruct.m):
        return -1
   
      for i in range(0,self.BCHstruct.n):
        self.BCHstruct.a_pow_tab[i]=x
        self.BCHstruct.a_log_tab[x]=i
        if i and x==1:
         return -1
        x*= 2
        if (x & k):
          x=x^poly

      self.BCHstruct.a_log_tab[0]=0
      self.BCHstruct.a_pow_tab[self.BCHstruct.n]=1



      n=0
      g=self.GFpoly(deg=0)   
      g.c=[0]*((m*t)+1) 
      roots=[0]*(self.BCHstruct.n+1)
      genpoly=[0]*self.DIV_ROUND_UP(m*t+1,32)

      # enum all roots
      for i in range(0,t):
         r=2*i+1
         for j in range(0,m):
           roots[r]=1
           r=self.mod(2*r)

      # build g(x)
      g.deg=0
      g.c[0]=1
      for i in range(0,self.BCHstruct.n):
        if roots[i]:
          r=self.BCHstruct.a_pow_tab[i]
          g.c[g.deg+1]=1
          for j in range(g.deg,0,-1):
              g.c[j]=self.gf_mul(g.c[j],r)^g.c[j-1]
          g.c[0]=self.gf_mul(g.c[0],r)
          g.deg += 1

      # store
      n = g.deg+1
      i = 0

      while (n>0) :

         if n>32:
            nbits=32
         else:
            nbits=n

         word=0
         for j in range (0,nbits):
           if g.c[n-1-j] :
               word = word | pow(2,31-j)
         genpoly[i]=word
         i += 1
         n -= nbits
      self.BCHstruct.ecc_bits=g.deg

      self.build_mod8_tables(genpoly);


      sum=0
      ak=0
      for i in range(0,m):
        for j in range(0,m):
          sum = sum ^ self.a_pow(i*pow(2,j))
        if sum: 
          ak=self.BCHstruct.a_pow_tab[i]
          break

      x=0
      xi=[0] * 31
      remaining=m

      while (x<= self.BCHstruct.n and remaining):
         y=self.gf_sqr(x)^x
         for i in range(0,2):
            r=self.a_log(y)
            if (y and (r<m) and not xi[r]):
              self.BCHstruct.xi_tab[r]=x
              xi[r]=1
              remaining -=1
              break
            y=y^ak
         x += 1




      
