class O2O:
    def __init__(self, data):
        self.vendor_id=data["vendor id"]
        self.uniq_subp=data["subpackage"].unique()
        self.uniq_p=data["package"].unique()
        self.uniq_venid=data["vendor id"].unique()
        self.data=data
    def count_subp_venid(self):
        data_ven_id_subp=self.data.groupby("vendor id")["subpackage"].nunique()
        return(data_ven_id_subp)
    
    def count_pack_venid(self):
        data_ven_id_p=self.data.groupby("vendor id")["package"].nunique()
        return(data_ven_id_p)
    def ven_dict_subp (self):
        ven_dict_subp={}
        data_ven_id_subp=O2O.count_subp_venid(self)
        for i in data_ven_id_subp.unique():
            ven_dict_subp[i]=data_ven_id_subp[data_ven_id_subp.values==i].index
        return ven_dict_subp                
    def ven_dict_p(self):
        ven_dict_p={}
        data_ven_id_p=O2O.count_pack_venid(self)
        for i in data_ven_id_p.unique():
            ven_dict_p[i]=data_ven_id_p[data_ven_id_p.values==i].index
        return ven_dict_p
    def O2N_subp(self, n):
        ven_dict_subp=O2O.ven_dict_subp(self)
        list1=list(ven_dict_subp.get(n))
        O2N_subp=self.data[self.data["vendor id"].isin(list1)]
        return O2N_subp
    def O2N_p(self, n):
        ven_dict_p=O2O.ven_dict_p(self)
        list2=list(ven_dict_p.get(n))
        O2N_p=self.data[self.data["vendor id"].isin(list2)]
        return O2N_p
        
class result(O2O):
    def __init__(self, vendorData, testData):
        self.ven_data=vendorData
        self.test_data=testData
    def result_O2O(self):
        ven_data=O2O(self.ven_data)
        db_subp=ven_data.O2N_subp(1)
        db_p=ven_data.O2N_p(1)
        p_Match=[]
        sub_p_Match=[]
        reassign_pack=[]
        reassign_subpack=[]
        for i in self.test_data["vendor id"].values:
            if i in db_p["vendor id"].values:
                p_Match.append(1)
                if i in db_subp["vendor id"].values:
                    sub_p_Match.append(1)	
                    reassign_pack.append(db_subp[db_subp["vendor id"]==i]["package"].unique().flatten()[0])
                    reassign_subpack.append(db_subp[db_subp["vendor id"]==i]["subpackage"].unique().flatten()[0])
                else:
                    sub_p_Match.append(0)
                    reassign_pack.append(db_p[db_p["vendor id"]==i]["package"].unique().flatten()[0])
                    reassign_subpack.append("Unassigned")
            else:
                p_Match.append(0)
                sub_p_Match.append(0)
                reassign_subpack.append("Unassigned")
                reassign_pack.append("Unassigned") 
        self.test_data["p_Match"]=p_Match
        self.test_data["sub_p_Match"]=sub_p_Match
        self.test_data["reassign_pack"]=reassign_pack
        self.test_data["reassign_subpack"]=reassign_subpack
        return(self.test_data)
