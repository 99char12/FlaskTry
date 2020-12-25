from firebase import firebase 
       
class DataEntrySignin(object):
    def __init__(self,email,password,eid,role):
        self.email=email
        self.password=password
        self.eid=eid
        self.role=role
    
    def register(self):
        firebas = firebase.FirebaseApplication('https://farmsistantfinal.firebaseio.com/',None)
        data={'email':self.email,'password':self.password,'role':self.role,'employeeId':self.eid}
        result = firebas.post('Registration_web/',data)
        #print(result)
    
    @classmethod
    def validate(cls,emid,email,password):
        firebas = firebase.FirebaseApplication('https://farmsistantfinal.firebaseio.com/',None)
        result=firebas.get('Registration_web/',None)
        l1,l2,l3=[],[],[]
        for i in result.values():
            l1.append(i['employeeId'])
            l2.append(i['email'])
            l3.append(i['password'])
        c=0    
        for i in range(len(l1)):
            if(l1[i]==emid and l2[i]==email and l3[i]==password):
                c+=1
        if(c==0):
            return 0
        else:
            return 1
                
        
    @classmethod
    def showIncome(cls):
        firebas = firebase.FirebaseApplication('https://farmsistantfinal.firebaseio.com/',None)
        result=firebas.get('Previous/',None)
        m=0
        n=0
        for i in result.values():
            m=i['overall_price']
            n=i['yield_quintals']
        l=[]
        l.append(m)
        l.append(n)
        return l
        
     