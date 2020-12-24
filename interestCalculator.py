class InterestCalculator():
    def __init__(self,l):
        self.l=l
           
    def showIncome(self):
        acre=self.l[0]
        amt = int(self.l[1])
        scheme= self.l[2]
        time = int(self.l[3])
        inc = float(self.l[4])
        
        inter = []
        interest_per_year = 0.07 * amt;
        t=time//12;
        s= amt + (interest_per_year)*time;
        res = s/time
        return res
        
        