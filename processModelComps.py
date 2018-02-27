
# coding: utf-8

# In[1]:


import csv
import re


# In[21]:


class Model:
    def __init__(self,name,formula):
        self.name = name
        self.formula = formula
        #A list of tuples of effect and significance level
        self.effects = []
    
    def add_effect(self,factor,effect):
        if effect == "   ":
            self.effects.append((factor,"ns"))
        else:
            self.effects.append((factor,effect))
            
def print_file(filename):
    #print contents for debugging
    with open(filename,'rU') as inputfile:
        active_model = None
        for row in csv.reader(inputfile):
            print(row)
        
def extract_models(filename):
    #process text file to extract models
    models = []
    with open(filename,'rU') as inputfile:
        found_intercept_line = False
        for row in csv.reader(inputfile):
            if (len(row)==1):
                if (row[0].startswith("---") or len(row)==0) and found_intercept_line:
                    print("End of effects")
                    found_intercept_line = False
                    models.append(model)
                modelName = "name missing"
                m = re.match("> summary\(fit[0-9]+[a-z]*\)", row[0])
                if m:
                    modelName = row[0].replace('> summary(','')
                    modelName = modelName.replace(')','')
                    print(modelName)
                if row[0].startswith("Formula"):
                    formula = row[0].replace('Formula: ','')
                    print(formula)
                    model = Model(modelName,formula)
                    modelName = "name missing"
                    #NOTE: THERE IS AN ISSUE HERE THAT SOME OF THEM DON'T START WITH > summary(XXX)
                if found_intercept_line:
                    row_string = row[0].replace('< ','')
                    vals = row_string.split()
                    factor = vals[0]
                    if len(vals)==6:
                        effect = vals[5]
                    else:
                        effect = "ns"
                    model.add_effect(factor,effect)
                    print(factor,effect)
                if row[0].startswith("(Intercept)"):
                    found_intercept_line = True
                    print("Start of effects")
    return models

def create_factor_list(models):
    #Get list of factors (print as it goes to debug)
    factor_list = []
    for model in models:
        print(model.name,model.formula)
        for (factor,effect) in model.effects:
            print(factor,effect)
            if factor not in factor_list:
                factor_list.append(factor)

    print(factor_list)
    return factor_list

def csv_output(models,factor_list,output_filename):
    #print CSV file
    header = ["Model #","Formula"]+factor_list
    with open('output_filename.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        for model in models:
            row = [model.name,model.formula]
            model_factors = []
            for (factor,effect) in model.effects:
                model_factors.append(factor)
            for factorname in factor_list:
                if factorname in model_factors:
                    for (factor,effect) in model.effects:
                        if factor == factorname:
                            row.append(effect)
                else:
                    row.append("")
            wr.writerow(row)


# In[15]:


#RELJ Models
relj_textfile = 'modelsummaries20171029_RELJ.txt'
print_file(relj_textfile)


# In[16]:


relj_models = extract_models(relj_textfile)


# In[17]:


relj_factors = create_factor_list(relj_models)


# In[18]:


csv_output(relj_models,relj_factors,'relj_output.csv')


# In[19]:


#Do the same with GEO models
geo_textfile = 'TA_GEO_MODELS201711 copy.txt'
print_file(geo_textfile)


# In[22]:


geo_models = extract_models(geo_textfile)


# In[23]:


geo_factors = create_factor_list(geo_models)


# In[24]:


csv_output(geo_models,geo_factors,'geo_output.csv')

