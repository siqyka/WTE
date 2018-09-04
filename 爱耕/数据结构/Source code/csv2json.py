import json
import csv



class CsvJson():

    def judgment(self,data):
        judgment=[]
        for i in data:
            if i:
                judgment.append(True)
            else:
                judgment.append(False) 
        return judgment

    def save_json(self,data):
        with open('a.json','w',encoding='utf-8') as f:
            f.write(json.dumps(data,indent=4,ensure_ascii=False))

    def csv2json(self,file_path):
        dic={}
        csv_reader = csv.reader(open(file_path,encoding='utf-8'))
        for row in csv_reader:
            jg=self.judgment(row)
            if jg[0]:
                s1=row[0]
            if jg[1]:
                s2=row[1]
            if jg[2]:
                s3=row[2]


            if jg==[1,1,1,1]:
                dic[row[0]]=[{row[1]:[{row[2]:[row[3]]}]}]
            if jg==[0,1,1,1]:
                dic[s1].append({row[1]:[{row[2]:[row[3]]}]})
            if jg==[0,0,1,1]:
                dic[s1][-1][s2].append({row[2]:[row[3]]})
            if jg==[0,0,0,1]:
                dic[s1][-1][s2][-1][s3].append(row[3])
        return dic

def main():
    cj=CsvJson()
    dic=cj.csv2json('../history.csv')
    cj.save_json(dic)
    
if __name__ == '__main__':
    main()

