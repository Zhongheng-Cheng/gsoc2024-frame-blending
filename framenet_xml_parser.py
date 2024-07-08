from bs4 import BeautifulSoup
import re
import json
import os
from tqdm import tqdm

def get_fr_name(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    frame_name=Bs_data.find('frame').get('name')
    if len(frame_name)!=0:
        frame_name=frame_name.strip()
        return frame_name
    else:
        return "no frame name"

def get_fr_def(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    b_unique = Bs_data.find_all('definition')
    if len(b_unique)!=0:
        fr_def=str(b_unique[0]).replace('&lt;','<').replace('&gt;','>')
        min_no=0
        expos=fr_def.find('<ex>')
        if expos==-1:
            expos=214748
        defpos=fr_def.find('</def-root>')
        if defpos==-1:
            defpos=214748
        if min(expos,defpos)==214748:
            min_no=fr_def.find('<def-root>')+11
        else:
            min_no=min(expos,defpos)
        fr_def=fr_def[fr_def.find('<def-root>')+10:min_no].replace('\n',' ').strip()
        fr_def=re.compile(r'<[^>]+>').sub('', fr_def).strip()
        return fr_def
    else:
        return "no frame definition"

def get_fe_def(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    
    fe_unique = Bs_data.find_all('FE')
    if len(fe_unique)!=0:
        for i in range(len(fe_unique)):
            name=fe_unique[i].get('name').replace("-"," ").replace("_"," ").strip()
            value=fe_unique[i].find('definition')
            value=str(value).replace('&lt;','<').replace('&gt;','>')
            marker=value.find('<ex>')
            if marker==-1:
                marker=214748
            value=value[:min(marker,len(value))].replace('\n',' ')
            value=re.compile(r'<[^>]+>').sub('', value).strip()
            yield name,value
    else:
        return "no frame element found","no frame element definition found"

def get_lex_udef(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    
    le_unique = Bs_data.find_all('lexUnit')
    if len(le_unique)!=0:
        for i in le_unique:
            name=str(i.get('name')).replace("-"," ").replace("_"," ").strip()
            value=str(i.find("definition")).replace('&lt;','<').replace('&gt;','>').replace('\n',' ')
            value=re.compile(r'<[^>]+>').sub('', value).strip()
            yield name,value
    else:
        return "no lex unit","no lex unit def"
    
def whole_tag(text,tag,at="name="): #inner content,remaining part, attribute data
    value=text[text.find('>',text.find(f"<{tag}"))+1:text.find(f"</{tag}>")]
    if text.find(at)!=-1:
        att_name=text[text.find(at)+6:text.find('">',text.find(f"<{tag}"))]
    else:
        att_name=""
    return value.strip(),text[text.find(f"</{tag}>")+len(tag)+3:].strip(),att_name.strip()

def get_fr_ex(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    Bs_data=str(Bs_data).replace('&lt;','<').replace('&gt;','>')
    Bs_data = BeautifulSoup(Bs_data, "xml")

    fe_unique=Bs_data.find_all('ex')
    if len(fe_unique)!=-1:
        for i in fe_unique:
            value2=str(i).replace('&lt;','<').replace('&gt;','>').replace('\n',' ')
            example=re.compile(r'<[^>]+>').sub('', value2[4:-5]).strip()
            yield example
            if value2.find('<t>')!=-1:
                frame_rep=value2[value2.find('<t>')+3:value2.find('</t>')].strip()
                yield frame_rep,f"the lexical unit of {get_fr_name(name)}"
            temp=value2
            for j in range(value2.count('<fex')):
                v,temp,att=whole_tag(temp,'fex')
                fele=att.replace('&lt;','<').replace('&gt;','>').replace('\n',' ')
                yield v,fele
    else: 
        return "no example found"
    
def get_fr_rel(name):
    with open(name, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    le_unique = Bs_data.find_all('frameRelation')
    joint=" ".join(str(i) for i in le_unique)
    if joint.find('<relatedFrame')!=-1:
        for i in le_unique:
            if len(i.find_all('relatedFrame'))>0:
                _,_,fr_type=whole_tag(str(i),"frameRelation","type=")
                fr_type=fr_type.replace("-"," ").replace("_"," ").strip()
                relation=", ".join(re.compile(r'<[^>]+>').sub('', str(j)).strip() for j in i.find_all('relatedFrame'))
                relation=relation.strip()
                yield fr_type,relation
    else:
        return "no related frame type","no related frame name"

def xml_parser(name):
    out=dict()
    
    #frame name
    out['frame_name']=get_fr_name(name)
    
    #frame def
    out['frame_def']=get_fr_def(name)
    
    #frame element desc
    fe_dict=dict()
    for i in get_fe_def(name):
        fe_dict[i[0]]=i[1]
    out['fe_def']=fe_dict
    
    #frame lexical unit & def
    le_dict=dict()
    for i in get_lex_udef(name):
        le_dict[i[0]]=i[1]
    out['lexical']=le_dict
    
    #frame examples
    if get_fr_ex(name)=="no example found":
        out['examples']="no example found"
    else:
        ex=""
        fe_dict_in=dict()
        fe_dict_out=dict()
        for i in get_fr_ex(name):
            if type(i)==type("asd") and len(fe_dict_in)>0:
                fe_dict_out[ex]=fe_dict_in
            if type(i)==type("asd"):
                ex=i
                fe_dict_in=dict()
            elif type(i)==type(('a','b','v')):
                fe_dict_in[i[0]]=i[1]
            else:
                out['examples']="no example/error"
                break
        out['examples']=fe_dict_out
    
    #frame relation
    frel_dict=dict()
    for i in get_fr_rel(name):
        frel_dict[i[0]]=i[1]
    out['fr_rel']=frel_dict
    
    return out

def xml_to_json(input_path, output_path):
    with open(output_path, 'w') as fo:
        json.dump(xml_parser(input_path), fo, indent=4)
    return


if __name__=="__main__":
    xml_folder_name = "frame"
    json_folder_name = "frame_json"
    if not os.path.exists(json_folder_name):
        os.makedirs(json_folder_name)
    file_names = [file for file in os.listdir(xml_folder_name) if file[-4:] == ".xml"]
    progress_bar = tqdm(total=len(file_names), desc="Parsing")
    for file in file_names:
        xml_to_json(f"{xml_folder_name}/{file}", f"{json_folder_name}/{file.replace('.xml', '.json')}")
        progress_bar.update(1)
    progress_bar.close()
    print("Finished")

