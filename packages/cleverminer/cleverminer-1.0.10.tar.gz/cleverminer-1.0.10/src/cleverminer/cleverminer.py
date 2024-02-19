import sys #line:54
import time #line:55
import copy #line:56
from time import strftime #line:58
from time import gmtime #line:59
import pandas as pd #line:61
import numpy #line:62
from pandas .api .types import CategoricalDtype #line:63
import progressbar #line:65
import re #line:66
class cleverminer :#line:67
    version_string ="1.0.10"#line:69
    def __init__ (OOO000O000OO0OOOO ,**OO000OO00OOOOOOO0 ):#line:71
        OOO000O000OO0OOOO ._print_disclaimer ()#line:72
        OOO000O000OO0OOOO .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:81
        OOO000O000OO0OOOO .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:89
        OOO000O000OO0OOOO .df =None #line:90
        OOO000O000OO0OOOO .kwargs =None #line:91
        if len (OO000OO00OOOOOOO0 )>0 :#line:92
            OOO000O000OO0OOOO .kwargs =OO000OO00OOOOOOO0 #line:93
        OOO000O000OO0OOOO .verbosity ={}#line:94
        OOO000O000OO0OOOO .verbosity ['debug']=False #line:95
        OOO000O000OO0OOOO .verbosity ['print_rules']=False #line:96
        OOO000O000OO0OOOO .verbosity ['print_hashes']=True #line:97
        OOO000O000OO0OOOO .verbosity ['last_hash_time']=0 #line:98
        OOO000O000OO0OOOO .verbosity ['hint']=False #line:99
        if "opts"in OO000OO00OOOOOOO0 :#line:100
            OOO000O000OO0OOOO ._set_opts (OO000OO00OOOOOOO0 .get ("opts"))#line:101
        if "opts"in OO000OO00OOOOOOO0 :#line:102
            if "verbose"in OO000OO00OOOOOOO0 .get ('opts'):#line:103
                OOO0O00OO00OO00O0 =OO000OO00OOOOOOO0 .get ('opts').get ('verbose')#line:104
                if OOO0O00OO00OO00O0 .upper ()=='FULL':#line:105
                    OOO000O000OO0OOOO .verbosity ['debug']=True #line:106
                    OOO000O000OO0OOOO .verbosity ['print_rules']=True #line:107
                    OOO000O000OO0OOOO .verbosity ['print_hashes']=False #line:108
                    OOO000O000OO0OOOO .verbosity ['hint']=True #line:109
                    OOO000O000OO0OOOO .options ['progressbar']=False #line:110
                elif OOO0O00OO00OO00O0 .upper ()=='RULES':#line:111
                    OOO000O000OO0OOOO .verbosity ['debug']=False #line:112
                    OOO000O000OO0OOOO .verbosity ['print_rules']=True #line:113
                    OOO000O000OO0OOOO .verbosity ['print_hashes']=True #line:114
                    OOO000O000OO0OOOO .verbosity ['hint']=True #line:115
                    OOO000O000OO0OOOO .options ['progressbar']=False #line:116
                elif OOO0O00OO00OO00O0 .upper ()=='HINT':#line:117
                    OOO000O000OO0OOOO .verbosity ['debug']=False #line:118
                    OOO000O000OO0OOOO .verbosity ['print_rules']=False #line:119
                    OOO000O000OO0OOOO .verbosity ['print_hashes']=True #line:120
                    OOO000O000OO0OOOO .verbosity ['last_hash_time']=0 #line:121
                    OOO000O000OO0OOOO .verbosity ['hint']=True #line:122
                    OOO000O000OO0OOOO .options ['progressbar']=False #line:123
                elif OOO0O00OO00OO00O0 .upper ()=='DEBUG':#line:124
                    OOO000O000OO0OOOO .verbosity ['debug']=True #line:125
                    OOO000O000OO0OOOO .verbosity ['print_rules']=True #line:126
                    OOO000O000OO0OOOO .verbosity ['print_hashes']=True #line:127
                    OOO000O000OO0OOOO .verbosity ['last_hash_time']=0 #line:128
                    OOO000O000OO0OOOO .verbosity ['hint']=True #line:129
                    OOO000O000OO0OOOO .options ['progressbar']=False #line:130
        OOO000O000OO0OOOO ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:131
        if not (OOO000O000OO0OOOO ._is_py310 ):#line:132
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:133
        else :#line:134
            if (OOO000O000OO0OOOO .verbosity ['debug']):#line:135
                print ("Python 3.10+ detected.")#line:136
        OOO000O000OO0OOOO ._initialized =False #line:137
        OOO000O000OO0OOOO ._init_data ()#line:138
        OOO000O000OO0OOOO ._init_task ()#line:139
        if len (OO000OO00OOOOOOO0 )>0 :#line:140
            if "df"in OO000OO00OOOOOOO0 :#line:141
                OOO000O000OO0OOOO ._prep_data (OO000OO00OOOOOOO0 .get ("df"))#line:142
            else :#line:143
                print ("Missing dataframe. Cannot initialize.")#line:144
                OOO000O000OO0OOOO ._initialized =False #line:145
                return #line:146
            OO0O00OO0OOOO00O0 =OO000OO00OOOOOOO0 .get ("proc",None )#line:147
            if not (OO0O00OO0OOOO00O0 ==None ):#line:148
                OOO000O000OO0OOOO ._calculate (**OO000OO00OOOOOOO0 )#line:149
            else :#line:151
                if OOO000O000OO0OOOO .verbosity ['debug']:#line:152
                    print ("INFO: just initialized")#line:153
                OOO00OO00O000000O ={}#line:154
                OO0OO0OOO0O0O0O00 ={}#line:155
                OO0OO0OOO0O0O0O00 ["varname"]=OOO000O000OO0OOOO .data ["varname"]#line:156
                OO0OO0OOO0O0O0O00 ["catnames"]=OOO000O000OO0OOOO .data ["catnames"]#line:157
                OOO00OO00O000000O ["datalabels"]=OO0OO0OOO0O0O0O00 #line:158
                OOO000O000OO0OOOO .result =OOO00OO00O000000O #line:159
        OOO000O000OO0OOOO ._initialized =True #line:161
    def _set_opts (O00OOO00OO0O0OOO0 ,OOO00OO0O0OO0000O ):#line:163
        if "no_optimizations"in OOO00OO0O0OO0000O :#line:164
            O00OOO00OO0O0OOO0 .options ['optimizations']=not (OOO00OO0O0OO0000O ['no_optimizations'])#line:165
            print ("No optimization will be made.")#line:166
        if "disable_progressbar"in OOO00OO0O0OO0000O :#line:167
            O00OOO00OO0O0OOO0 .options ['progressbar']=False #line:168
            print ("Progressbar will not be shown.")#line:169
        if "max_rules"in OOO00OO0O0OO0000O :#line:170
            O00OOO00OO0O0OOO0 .options ['max_rules']=OOO00OO0O0OO0000O ['max_rules']#line:171
        if "max_categories"in OOO00OO0O0OO0000O :#line:172
            O00OOO00OO0O0OOO0 .options ['max_categories']=OOO00OO0O0OO0000O ['max_categories']#line:173
            if O00OOO00OO0O0OOO0 .verbosity ['debug']==True :#line:174
                print (f"Maximum number of categories set to {O00OOO00OO0O0OOO0.options['max_categories']}")#line:175
        if "no_automatic_data_conversions"in OOO00OO0O0OO0000O :#line:176
            O00OOO00OO0O0OOO0 .options ['automatic_data_conversions']=not (OOO00OO0O0OO0000O ['no_automatic_data_conversions'])#line:177
            print ("No automatic data conversions will be made.")#line:178
        if "keep_df"in OOO00OO0O0OO0000O :#line:179
            O00OOO00OO0O0OOO0 .options ['keep_df']=OOO00OO0O0OO0000O ['keep_df']#line:180
    def _init_data (O0000O00O0O000O0O ):#line:183
        O0000O00O0O000O0O .data ={}#line:185
        O0000O00O0O000O0O .data ["varname"]=[]#line:186
        O0000O00O0O000O0O .data ["catnames"]=[]#line:187
        O0000O00O0O000O0O .data ["vtypes"]=[]#line:188
        O0000O00O0O000O0O .data ["dm"]=[]#line:189
        O0000O00O0O000O0O .data ["rows_count"]=int (0 )#line:190
        O0000O00O0O000O0O .data ["data_prepared"]=0 #line:191
    def _init_task (O0000OO000OO0O0OO ):#line:193
        if "opts"in O0000OO000OO0O0OO .kwargs :#line:195
            O0000OO000OO0O0OO ._set_opts (O0000OO000OO0O0OO .kwargs .get ("opts"))#line:196
        O0000OO000OO0O0OO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:206
        O0000OO000OO0O0OO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:210
        O0000OO000OO0O0OO .rulelist =[]#line:211
        O0000OO000OO0O0OO .stats ['total_cnt']=0 #line:213
        O0000OO000OO0O0OO .stats ['total_valid']=0 #line:214
        O0000OO000OO0O0OO .stats ['control_number']=0 #line:215
        O0000OO000OO0O0OO .result ={}#line:216
        O0000OO000OO0O0OO ._opt_base =None #line:217
        O0000OO000OO0O0OO ._opt_relbase =None #line:218
        O0000OO000OO0O0OO ._opt_base1 =None #line:219
        O0000OO000OO0O0OO ._opt_relbase1 =None #line:220
        O0000OO000OO0O0OO ._opt_base2 =None #line:221
        O0000OO000OO0O0OO ._opt_relbase2 =None #line:222
        OOOOO00OOOO0000O0 =None #line:223
        if not (O0000OO000OO0O0OO .kwargs ==None ):#line:224
            OOOOO00OOOO0000O0 =O0000OO000OO0O0OO .kwargs .get ("quantifiers",None )#line:225
            if not (OOOOO00OOOO0000O0 ==None ):#line:226
                for O0OO000000000000O in OOOOO00OOOO0000O0 .keys ():#line:227
                    if O0OO000000000000O .upper ()=='BASE':#line:228
                        O0000OO000OO0O0OO ._opt_base =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:229
                    if O0OO000000000000O .upper ()=='RELBASE':#line:230
                        O0000OO000OO0O0OO ._opt_relbase =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:231
                    if (O0OO000000000000O .upper ()=='FRSTBASE')|(O0OO000000000000O .upper ()=='BASE1'):#line:232
                        O0000OO000OO0O0OO ._opt_base1 =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:233
                    if (O0OO000000000000O .upper ()=='SCNDBASE')|(O0OO000000000000O .upper ()=='BASE2'):#line:234
                        O0000OO000OO0O0OO ._opt_base2 =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:235
                    if (O0OO000000000000O .upper ()=='FRSTRELBASE')|(O0OO000000000000O .upper ()=='RELBASE1'):#line:236
                        O0000OO000OO0O0OO ._opt_relbase1 =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:237
                    if (O0OO000000000000O .upper ()=='SCNDRELBASE')|(O0OO000000000000O .upper ()=='RELBASE2'):#line:238
                        O0000OO000OO0O0OO ._opt_relbase2 =OOOOO00OOOO0000O0 .get (O0OO000000000000O )#line:239
            else :#line:240
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:241
        else :#line:242
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:243
    def mine (O0O0O000O0O000OO0 ,**O0OOOOOO0O000O00O ):#line:246
        if not (O0O0O000O0O000OO0 ._initialized ):#line:247
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:248
            return #line:249
        O0O0O000O0O000OO0 .kwargs =None #line:250
        if len (O0OOOOOO0O000O00O )>0 :#line:251
            O0O0O000O0O000OO0 .kwargs =O0OOOOOO0O000O00O #line:252
        O0O0O000O0O000OO0 ._init_task ()#line:253
        if len (O0OOOOOO0O000O00O )>0 :#line:254
            O0OOO00O00O0O00O0 =O0OOOOOO0O000O00O .get ("proc",None )#line:255
            if not (O0OOO00O00O0O00O0 ==None ):#line:256
                O0O0O000O0O000OO0 ._calc_all (**O0OOOOOO0O000O00O )#line:257
            else :#line:258
                print ("Rule mining procedure missing")#line:259
    def _get_ver (OOOO0OO0OOOO0O0O0 ):#line:262
        return OOOO0OO0OOOO0O0O0 .version_string #line:263
    def _print_disclaimer (O00OOOOOO00OO0O00 ):#line:265
        print (f"Cleverminer version {O00OOOOOO00OO0O00._get_ver()}.")#line:267
    def _automatic_data_conversions (O0OO0O000O0OOOO00 ,O00O0OO0O0OOO0O00 ):#line:273
        print ("Automatically reordering numeric categories ...")#line:274
        for OO0OOO00O0OOOOO0O in range (len (O00O0OO0O0OOO0O00 .columns )):#line:275
            if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:276
                print (f"#{OO0OOO00O0OOOOO0O}: {O00O0OO0O0OOO0O00.columns[OO0OOO00O0OOOOO0O]} : {O00O0OO0O0OOO0O00.dtypes[OO0OOO00O0OOOOO0O]}.")#line:277
            try :#line:278
                O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]]=O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]].astype (str ).astype (float )#line:279
                if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:280
                    print (f"CONVERTED TO FLOATS #{OO0OOO00O0OOOOO0O}: {O00O0OO0O0OOO0O00.columns[OO0OOO00O0OOOOO0O]} : {O00O0OO0O0OOO0O00.dtypes[OO0OOO00O0OOOOO0O]}.")#line:281
                OO0O0O00OOO000OOO =pd .unique (O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]])#line:282
                O000O00000O0OO0O0 =True #line:283
                for O00O00OO0O0OOO00O in OO0O0O00OOO000OOO :#line:284
                    if O00O00OO0O0OOO00O %1 !=0 :#line:285
                        O000O00000O0OO0O0 =False #line:286
                if O000O00000O0OO0O0 :#line:287
                    O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]]=O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]].astype (int )#line:288
                    if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:289
                        print (f"CONVERTED TO INT #{OO0OOO00O0OOOOO0O}: {O00O0OO0O0OOO0O00.columns[OO0OOO00O0OOOOO0O]} : {O00O0OO0O0OOO0O00.dtypes[OO0OOO00O0OOOOO0O]}.")#line:290
                O0O0OOOO00O000OOO =pd .unique (O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]])#line:291
                OOO0O0OO0OO0OOOO0 =CategoricalDtype (categories =O0O0OOOO00O000OOO .sort (),ordered =True )#line:292
                O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]]=O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]].astype (OOO0O0OO0OO0OOOO0 )#line:293
                if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:294
                    print (f"CONVERTED TO CATEGORY #{OO0OOO00O0OOOOO0O}: {O00O0OO0O0OOO0O00.columns[OO0OOO00O0OOOOO0O]} : {O00O0OO0O0OOO0O00.dtypes[OO0OOO00O0OOOOO0O]}.")#line:295
            except :#line:297
                if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:298
                    print ("...cannot be converted to int")#line:299
                try :#line:300
                    OO0OO00O0OO0000O0 =O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]].unique ()#line:301
                    if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:302
                        print (f"Values: {OO0OO00O0OO0000O0}")#line:303
                    OO0O0OO0OO00OO0O0 =True #line:304
                    OO0O0000OO0OO000O =[]#line:305
                    for O00O00OO0O0OOO00O in OO0OO00O0OO0000O0 :#line:306
                        O0OOO00OO00OO0OOO =re .findall (r"-?\d+",O00O00OO0O0OOO00O )#line:309
                        if len (O0OOO00OO00OO0OOO )>0 :#line:311
                            OO0O0000OO0OO000O .append (int (O0OOO00OO00OO0OOO [0 ]))#line:312
                        else :#line:313
                            OO0O0OO0OO00OO0O0 =False #line:314
                    if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:315
                        print (f"Is ok: {OO0O0OO0OO00OO0O0}, extracted {OO0O0000OO0OO000O}")#line:316
                    if OO0O0OO0OO00OO0O0 :#line:317
                        OO00OOOOOOO0OO0O0 =copy .deepcopy (OO0O0000OO0OO000O )#line:318
                        OO00OOOOOOO0OO0O0 .sort ()#line:319
                        OOO0O0O0O0O00O00O =[]#line:321
                        for OO0O000O0O0O0OOOO in OO00OOOOOOO0OO0O0 :#line:322
                            OOOO0O0OO0O000000 =OO0O0000OO0OO000O .index (OO0O000O0O0O0OOOO )#line:323
                            OOO0O0O0O0O00O00O .append (OO0OO00O0OO0000O0 [OOOO0O0OO0O000000 ])#line:325
                        if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:326
                            print (f"Sorted list: {OOO0O0O0O0O00O00O}")#line:327
                        OOO0O0OO0OO0OOOO0 =CategoricalDtype (categories =OOO0O0O0O0O00O00O ,ordered =True )#line:328
                        O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]]=O00O0OO0O0OOO0O00 [O00O0OO0O0OOO0O00 .columns [OO0OOO00O0OOOOO0O ]].astype (OOO0O0OO0OO0OOOO0 )#line:329
                except :#line:332
                    if O0OO0O000O0OOOO00 .verbosity ['debug']:#line:333
                        print ("...cannot extract numbers from all categories")#line:334
    print ("Automatically reordering numeric categories ...done")#line:336
    def _prep_data (OO0OO0OO0O0O00O00 ,O00O0O000000O0OOO ):#line:338
        print ("Starting data preparation ...")#line:339
        OO0OO0OO0O0O00O00 ._init_data ()#line:340
        OO0OO0OO0O0O00O00 .stats ['start_prep_time']=time .time ()#line:341
        if OO0OO0OO0O0O00O00 .options ['automatic_data_conversions']:#line:342
            OO0OO0OO0O0O00O00 ._automatic_data_conversions (O00O0O000000O0OOO )#line:343
        OO0OO0OO0O0O00O00 .data ["rows_count"]=O00O0O000000O0OOO .shape [0 ]#line:344
        for O0O0O0OOOO0000OOO in O00O0O000000O0OOO .select_dtypes (exclude =['category']).columns :#line:345
            O00O0O000000O0OOO [O0O0O0OOOO0000OOO ]=O00O0O000000O0OOO [O0O0O0OOOO0000OOO ].apply (str )#line:346
        try :#line:347
            O000OOO0OO0O0000O =pd .DataFrame .from_records ([(O0000OOOOOOOO000O ,O00O0O000000O0OOO [O0000OOOOOOOO000O ].nunique ())for O0000OOOOOOOO000O in O00O0O000000O0OOO .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:349
        except :#line:350
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:351
            O00O000O0O000OOO0 =""#line:352
            try :#line:353
                for O0O0O0OOOO0000OOO in O00O0O000000O0OOO .columns :#line:354
                    O00O000O0O000OOO0 =O0O0O0OOOO0000OOO #line:355
                    print (f"...column {O0O0O0OOOO0000OOO} has {int(O00O0O000000O0OOO[O0O0O0OOOO0000OOO].nunique())} values")#line:356
            except :#line:357
                print (f"... detected : column {O00O000O0O000OOO0} has unsupported type: {type(O00O0O000000O0OOO[O0O0O0OOOO0000OOO])}.")#line:358
                exit (1 )#line:359
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:360
            exit (1 )#line:361
        if OO0OO0OO0O0O00O00 .verbosity ['hint']:#line:364
            print ("Quick profile of input data: unique value counts are:")#line:365
            print (O000OOO0OO0O0000O )#line:366
            for O0O0O0OOOO0000OOO in O00O0O000000O0OOO .columns :#line:367
                if O00O0O000000O0OOO [O0O0O0OOOO0000OOO ].nunique ()<OO0OO0OO0O0O00O00 .options ['max_categories']:#line:368
                    O00O0O000000O0OOO [O0O0O0OOOO0000OOO ]=O00O0O000000O0OOO [O0O0O0OOOO0000OOO ].astype ('category')#line:369
                else :#line:370
                    print (f"WARNING: attribute {O0O0O0OOOO0000OOO} has more than {OO0OO0OO0O0O00O00.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:371
                    del O00O0O000000O0OOO [O0O0O0OOOO0000OOO ]#line:372
        for O0O0O0OOOO0000OOO in O00O0O000000O0OOO .columns :#line:374
            if O00O0O000000O0OOO [O0O0O0OOOO0000OOO ].nunique ()>OO0OO0OO0O0O00O00 .options ['max_categories']:#line:375
                print (f"WARNING: attribute {O0O0O0OOOO0000OOO} has more than {OO0OO0OO0O0O00O00.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:376
                del O00O0O000000O0OOO [O0O0O0OOOO0000OOO ]#line:377
        if OO0OO0OO0O0O00O00 .options ['keep_df']:#line:378
            if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:379
                print ("Keeping df.")#line:380
            OO0OO0OO0O0O00O00 .df =O00O0O000000O0OOO #line:381
        print ("Encoding columns into bit-form...")#line:382
        OO0O0O00O0OO000O0 =0 #line:383
        O00O0000O0O0O000O =0 #line:384
        for O0000OOO0O0OOOO0O in O00O0O000000O0OOO :#line:385
            if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:387
                print ('Column: '+O0000OOO0O0OOOO0O )#line:388
            OO0OO0OO0O0O00O00 .data ["varname"].append (O0000OOO0O0OOOO0O )#line:389
            O000O0OOO00O0000O =pd .get_dummies (O00O0O000000O0OOO [O0000OOO0O0OOOO0O ])#line:390
            O0OOOO00OO00OO000 =0 #line:391
            if (O00O0O000000O0OOO .dtypes [O0000OOO0O0OOOO0O ].name =='category'):#line:392
                O0OOOO00OO00OO000 =1 #line:393
            OO0OO0OO0O0O00O00 .data ["vtypes"].append (O0OOOO00OO00OO000 )#line:394
            OO0000OOOOO0O00OO =0 #line:397
            OO0O0O0O0O0OOO0OO =[]#line:398
            OO00OOOO0O0O0000O =[]#line:399
            for O00OO0O0O0OOOOO00 in O000O0OOO00O0000O :#line:401
                if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:403
                    print ('....category : '+str (O00OO0O0O0OOOOO00 )+" @ "+str (time .time ()))#line:404
                OO0O0O0O0O0OOO0OO .append (O00OO0O0O0OOOOO00 )#line:405
                O0O0OOO0O00O0OO00 =int (0 )#line:406
                O0OO000O0OO000O0O =O000O0OOO00O0000O [O00OO0O0O0OOOOO00 ].values #line:407
                O0OOO0O00000000O0 =numpy .packbits (O0OO000O0OO000O0O ,bitorder ='little')#line:409
                O0O0OOO0O00O0OO00 =int .from_bytes (O0OOO0O00000000O0 ,byteorder ='little')#line:410
                OO00OOOO0O0O0000O .append (O0O0OOO0O00O0OO00 )#line:411
                OO0000OOOOO0O00OO +=1 #line:429
                O00O0000O0O0O000O +=1 #line:430
            OO0OO0OO0O0O00O00 .data ["catnames"].append (OO0O0O0O0O0OOO0OO )#line:432
            OO0OO0OO0O0O00O00 .data ["dm"].append (OO00OOOO0O0O0000O )#line:433
        print ("Encoding columns into bit-form...done")#line:435
        if OO0OO0OO0O0O00O00 .verbosity ['hint']:#line:436
            print (f"List of attributes for analysis is: {OO0OO0OO0O0O00O00.data['varname']}")#line:437
            print (f"List of category names for individual attributes is : {OO0OO0OO0O0O00O00.data['catnames']}")#line:438
        if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:439
            print (f"List of vtypes is (all should be 1) : {OO0OO0OO0O0O00O00.data['vtypes']}")#line:440
        OO0OO0OO0O0O00O00 .data ["data_prepared"]=1 #line:442
        print ("Data preparation finished.")#line:443
        if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:444
            print ('Number of variables : '+str (len (OO0OO0OO0O0O00O00 .data ["dm"])))#line:445
            print ('Total number of categories in all variables : '+str (O00O0000O0O0O000O ))#line:446
        OO0OO0OO0O0O00O00 .stats ['end_prep_time']=time .time ()#line:447
        if OO0OO0OO0O0O00O00 .verbosity ['debug']:#line:448
            print ('Time needed for data preparation : ',str (OO0OO0OO0O0O00O00 .stats ['end_prep_time']-OO0OO0OO0O0O00O00 .stats ['start_prep_time']))#line:449
    def _bitcount (O000O000O00000O00 ,O0O0000OO00O00O0O ):#line:451
        OO00O0O0OO0O000OO =None #line:452
        if (O000O000O00000O00 ._is_py310 ):#line:453
            OO00O0O0OO0O000OO =O0O0000OO00O00O0O .bit_count ()#line:454
        else :#line:455
            OO00O0O0OO0O000OO =bin (O0O0000OO00O00O0O ).count ("1")#line:456
        return OO00O0O0OO0O000OO #line:457
    def _verifyCF (O00O00000000O0000 ,_O0O0O000O00O0000O ):#line:460
        OOO0OO00000O00000 =O00O00000000O0000 ._bitcount (_O0O0O000O00O0000O )#line:461
        O0000OO00OOOO0O0O =[]#line:462
        O0O0OO00OOO00OOO0 =[]#line:463
        O000OO0OO0000OOO0 =0 #line:464
        O0OO0OO000OO0000O =0 #line:465
        O0OOOOOO00OOO000O =0 #line:466
        OOOOO00OOOO0O0000 =0 #line:467
        O0O0OOOO0000O0OO0 =0 #line:468
        OOOOOO0OOOOO0O0OO =0 #line:469
        O0O000O0OOO000OO0 =0 #line:470
        OOOOO00O0000000OO =0 #line:471
        O00000OO0O00O00OO =0 #line:472
        OO00OO0000O0OOO0O =None #line:473
        O00O0O0OOO0O000O0 =None #line:474
        O0OO0OOOOOO00OOO0 =None #line:475
        if ('min_step_size'in O00O00000000O0000 .quantifiers ):#line:476
            OO00OO0000O0OOO0O =O00O00000000O0000 .quantifiers .get ('min_step_size')#line:477
        if ('min_rel_step_size'in O00O00000000O0000 .quantifiers ):#line:478
            O00O0O0OOO0O000O0 =O00O00000000O0000 .quantifiers .get ('min_rel_step_size')#line:479
            if O00O0O0OOO0O000O0 >=1 and O00O0O0OOO0O000O0 <100 :#line:480
                O00O0O0OOO0O000O0 =O00O0O0OOO0O000O0 /100 #line:481
        O0O0OO000O0000O0O =0 #line:482
        OO0OOOOO00OOO0O00 =0 #line:483
        OOO000OOOO00OOOO0 =[]#line:484
        if ('aad_weights'in O00O00000000O0000 .quantifiers ):#line:485
            O0O0OO000O0000O0O =1 #line:486
            OO00OOOOOOO0O0OO0 =[]#line:487
            OOO000OOOO00OOOO0 =O00O00000000O0000 .quantifiers .get ('aad_weights')#line:488
        OOO000OO0O0O0O00O =O00O00000000O0000 .data ["dm"][O00O00000000O0000 .data ["varname"].index (O00O00000000O0000 .kwargs .get ('target'))]#line:489
        def O0OO0O0OO0O00O0OO (OO00O00OO00OOOO0O ,OO0OOO0O0O0O0OOOO ):#line:490
            OO0OOO0O0O0OOO0OO =True #line:491
            if (OO00O00OO00OOOO0O >OO0OOO0O0O0O0OOOO ):#line:492
                if not (OO00OO0000O0OOO0O is None or OO00O00OO00OOOO0O >=OO0OOO0O0O0O0OOOO +OO00OO0000O0OOO0O ):#line:493
                    OO0OOO0O0O0OOO0OO =False #line:494
                if not (O00O0O0OOO0O000O0 is None or OO00O00OO00OOOO0O >=OO0OOO0O0O0O0OOOO *(1 +O00O0O0OOO0O000O0 )):#line:495
                    OO0OOO0O0O0OOO0OO =False #line:496
            if (OO00O00OO00OOOO0O <OO0OOO0O0O0O0OOOO ):#line:497
                if not (OO00OO0000O0OOO0O is None or OO00O00OO00OOOO0O <=OO0OOO0O0O0O0OOOO -OO00OO0000O0OOO0O ):#line:498
                    OO0OOO0O0O0OOO0OO =False #line:499
                if not (O00O0O0OOO0O000O0 is None or OO00O00OO00OOOO0O <=OO0OOO0O0O0O0OOOO *(1 -O00O0O0OOO0O000O0 )):#line:500
                    OO0OOO0O0O0OOO0OO =False #line:501
            return OO0OOO0O0O0OOO0OO #line:502
        for O0000OOOOO0O00O0O in range (len (OOO000OO0O0O0O00O )):#line:503
            O0OO0OO000OO0000O =O000OO0OO0000OOO0 #line:505
            O000OO0OO0000OOO0 =O00O00000000O0000 ._bitcount (_O0O0O000O00O0000O &OOO000OO0O0O0O00O [O0000OOOOO0O00O0O ])#line:506
            O0000OO00OOOO0O0O .append (O000OO0OO0000OOO0 )#line:507
            if O0000OOOOO0O00O0O >0 :#line:508
                if (O000OO0OO0000OOO0 >O0OO0OO000OO0000O ):#line:509
                    if (O0OOOOOO00OOO000O ==1 )and (O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O )):#line:510
                        OOOOO00O0000000OO +=1 #line:511
                    else :#line:512
                        if O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O ):#line:513
                            OOOOO00O0000000OO =1 #line:514
                        else :#line:515
                            OOOOO00O0000000OO =0 #line:516
                    if OOOOO00O0000000OO >OOOOO00OOOO0O0000 :#line:517
                        OOOOO00OOOO0O0000 =OOOOO00O0000000OO #line:518
                    O0OOOOOO00OOO000O =1 #line:519
                    if O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O ):#line:520
                        OOOOOO0OOOOO0O0OO +=1 #line:521
                if (O000OO0OO0000OOO0 <O0OO0OO000OO0000O ):#line:522
                    if (O0OOOOOO00OOO000O ==-1 )and (O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O )):#line:523
                        O00000OO0O00O00OO +=1 #line:524
                    else :#line:525
                        if O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O ):#line:526
                            O00000OO0O00O00OO =1 #line:527
                        else :#line:528
                            O00000OO0O00O00OO =0 #line:529
                    if O00000OO0O00O00OO >O0O0OOOO0000O0OO0 :#line:530
                        O0O0OOOO0000O0OO0 =O00000OO0O00O00OO #line:531
                    O0OOOOOO00OOO000O =-1 #line:532
                    if O0OO0O0OO0O00O0OO (O000OO0OO0000OOO0 ,O0OO0OO000OO0000O ):#line:533
                        O0O000O0OOO000OO0 +=1 #line:534
                if (O000OO0OO0000OOO0 ==O0OO0OO000OO0000O ):#line:535
                    O0OOOOOO00OOO000O =0 #line:536
                    O00000OO0O00O00OO =0 #line:537
                    OOOOO00O0000000OO =0 #line:538
            if (O0O0OO000O0000O0O ):#line:540
                OOOOO00OO0O0OOOOO =O00O00000000O0000 ._bitcount (OOO000OO0O0O0O00O [O0000OOOOO0O00O0O ])#line:541
                OO00OOOOOOO0O0OO0 .append (OOOOO00OO0O0OOOOO )#line:542
        if (O0O0OO000O0000O0O &sum (O0000OO00OOOO0O0O )>0 ):#line:544
            for O0000OOOOO0O00O0O in range (len (OOO000OO0O0O0O00O )):#line:545
                if OO00OOOOOOO0O0OO0 [O0000OOOOO0O00O0O ]>0 :#line:546
                    if O0000OO00OOOO0O0O [O0000OOOOO0O00O0O ]/sum (O0000OO00OOOO0O0O )>OO00OOOOOOO0O0OO0 [O0000OOOOO0O00O0O ]/sum (OO00OOOOOOO0O0OO0 ):#line:548
                        OO0OOOOO00OOO0O00 +=OOO000OOOO00OOOO0 [O0000OOOOO0O00O0O ]*((O0000OO00OOOO0O0O [O0000OOOOO0O00O0O ]/sum (O0000OO00OOOO0O0O ))/(OO00OOOOOOO0O0OO0 [O0000OOOOO0O00O0O ]/sum (OO00OOOOOOO0O0OO0 ))-1 )#line:549
        OOOOO0O00O00O00OO =True #line:552
        for OO00O0000O000OO0O in O00O00000000O0000 .quantifiers .keys ():#line:553
            if OO00O0000O000OO0O .upper ()=='BASE':#line:554
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=OOO0OO00000O00000 )#line:555
            if OO00O0000O000OO0O .upper ()=='RELBASE':#line:556
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=OOO0OO00000O00000 *1.0 /O00O00000000O0000 .data ["rows_count"])#line:557
            if OO00O0000O000OO0O .upper ()=='S_UP':#line:558
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=OOOOO00OOOO0O0000 )#line:559
            if OO00O0000O000OO0O .upper ()=='S_DOWN':#line:560
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=O0O0OOOO0000O0OO0 )#line:561
            if OO00O0000O000OO0O .upper ()=='S_ANY_UP':#line:562
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=OOOOO00OOOO0O0000 )#line:563
            if OO00O0000O000OO0O .upper ()=='S_ANY_DOWN':#line:564
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=O0O0OOOO0000O0OO0 )#line:565
            if OO00O0000O000OO0O .upper ()=='MAX':#line:566
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=max (O0000OO00OOOO0O0O ))#line:567
            if OO00O0000O000OO0O .upper ()=='MIN':#line:568
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=min (O0000OO00OOOO0O0O ))#line:569
            if OO00O0000O000OO0O .upper ()=='RELMAX':#line:570
                if sum (O0000OO00OOOO0O0O )>0 :#line:571
                    OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=max (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O ))#line:572
                else :#line:573
                    OOOOO0O00O00O00OO =False #line:574
            if OO00O0000O000OO0O .upper ()=='RELMAX_LEQ':#line:575
                if sum (O0000OO00OOOO0O0O )>0 :#line:576
                    OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )>=max (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O ))#line:577
                else :#line:578
                    OOOOO0O00O00O00OO =False #line:579
            if OO00O0000O000OO0O .upper ()=='RELMIN':#line:580
                if sum (O0000OO00OOOO0O0O )>0 :#line:581
                    OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=min (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O ))#line:582
                else :#line:583
                    OOOOO0O00O00O00OO =False #line:584
            if OO00O0000O000OO0O .upper ()=='RELMIN_LEQ':#line:585
                if sum (O0000OO00OOOO0O0O )>0 :#line:586
                    OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )>=min (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O ))#line:587
                else :#line:588
                    OOOOO0O00O00O00OO =False #line:589
            if OO00O0000O000OO0O .upper ()=='AAD':#line:590
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )<=OO0OOOOO00OOO0O00 )#line:591
            if OO00O0000O000OO0O .upper ()=='RELRANGE_LEQ':#line:593
                O00OO0O00O0O00O0O =O00O00000000O0000 .quantifiers .get (OO00O0000O000OO0O )#line:594
                if O00OO0O00O0O00O0O >=1 and O00OO0O00O0O00O0O <100 :#line:595
                    O00OO0O00O0O00O0O =O00OO0O00O0O00O0O *1.0 /100 #line:596
                O00OO000OOO00OOOO =min (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O )#line:597
                O0OO00OOOO0OO00OO =max (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O )#line:598
                OOOOO0O00O00O00OO =OOOOO0O00O00O00OO and (O00OO0O00O0O00O0O >=O0OO00OOOO0OO00OO -O00OO000OOO00OOOO )#line:599
        O0O00OOOO0OOOOOOO ={}#line:600
        if OOOOO0O00O00O00OO ==True :#line:601
            O00O00000000O0000 .stats ['total_valid']+=1 #line:603
            O0O00OOOO0OOOOOOO ["base"]=OOO0OO00000O00000 #line:604
            O0O00OOOO0OOOOOOO ["rel_base"]=OOO0OO00000O00000 *1.0 /O00O00000000O0000 .data ["rows_count"]#line:605
            O0O00OOOO0OOOOOOO ["s_up"]=OOOOO00OOOO0O0000 #line:606
            O0O00OOOO0OOOOOOO ["s_down"]=O0O0OOOO0000O0OO0 #line:607
            O0O00OOOO0OOOOOOO ["s_any_up"]=OOOOOO0OOOOO0O0OO #line:608
            O0O00OOOO0OOOOOOO ["s_any_down"]=O0O000O0OOO000OO0 #line:609
            O0O00OOOO0OOOOOOO ["max"]=max (O0000OO00OOOO0O0O )#line:610
            O0O00OOOO0OOOOOOO ["min"]=min (O0000OO00OOOO0O0O )#line:611
            if sum (O0000OO00OOOO0O0O )>0 :#line:614
                O0O00OOOO0OOOOOOO ["rel_max"]=max (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O )#line:615
                O0O00OOOO0OOOOOOO ["rel_min"]=min (O0000OO00OOOO0O0O )*1.0 /sum (O0000OO00OOOO0O0O )#line:616
            else :#line:617
                O0O00OOOO0OOOOOOO ["rel_max"]=0 #line:618
                O0O00OOOO0OOOOOOO ["rel_min"]=0 #line:619
            O0O00OOOO0OOOOOOO ["hist"]=O0000OO00OOOO0O0O #line:620
            if O0O0OO000O0000O0O :#line:621
                O0O00OOOO0OOOOOOO ["aad"]=OO0OOOOO00OOO0O00 #line:622
                O0O00OOOO0OOOOOOO ["hist_full"]=OO00OOOOOOO0O0OO0 #line:623
                O0O00OOOO0OOOOOOO ["rel_hist"]=[OO00000OOOO0OO0OO /sum (O0000OO00OOOO0O0O )for OO00000OOOO0OO0OO in O0000OO00OOOO0O0O ]#line:624
                O0O00OOOO0OOOOOOO ["rel_hist_full"]=[OOO0O000OOO0OOO0O /sum (OO00OOOOOOO0O0OO0 )for OOO0O000OOO0OOO0O in OO00OOOOOOO0O0OO0 ]#line:625
        return OOOOO0O00O00O00OO ,O0O00OOOO0OOOOOOO #line:627
    def _verifyUIC (OOOO0OOO0OOOO00OO ,_OO0OOOO000OO00000 ):#line:629
        OO00000O00000O000 ={}#line:630
        O00O0000OOOOO0000 =0 #line:631
        for O000OO0O000O0OOO0 in OOOO0OOO0OOOO00OO .task_actinfo ['cedents']:#line:632
            OO00000O00000O000 [O000OO0O000O0OOO0 ['cedent_type']]=O000OO0O000O0OOO0 ['filter_value']#line:634
            O00O0000OOOOO0000 =O00O0000OOOOO0000 +1 #line:635
        O0000O0OO000O000O =OOOO0OOO0OOOO00OO ._bitcount (_OO0OOOO000OO00000 )#line:637
        OOOO00O000OOOOOO0 =[]#line:638
        O0OOOO00O000OOO00 =0 #line:639
        O00OO0O0OO0O0OO00 =0 #line:640
        OO0OO00OO00O00OOO =0 #line:641
        OOO0OOO0OO00O0OOO =[]#line:642
        O000000OO0O0O0OO0 =[]#line:643
        if ('aad_weights'in OOOO0OOO0OOOO00OO .quantifiers ):#line:644
            OOO0OOO0OO00O0OOO =OOOO0OOO0OOOO00OO .quantifiers .get ('aad_weights')#line:645
            O00OO0O0OO0O0OO00 =1 #line:646
        OOO000O000000O00O =OOOO0OOO0OOOO00OO .data ["dm"][OOOO0OOO0OOOO00OO .data ["varname"].index (OOOO0OOO0OOOO00OO .kwargs .get ('target'))]#line:647
        for OOOOO0OO0O0OO000O in range (len (OOO000O000000O00O )):#line:648
            O00O0O0O0O0O00OO0 =O0OOOO00O000OOO00 #line:650
            O0OOOO00O000OOO00 =OOOO0OOO0OOOO00OO ._bitcount (_OO0OOOO000OO00000 &OOO000O000000O00O [OOOOO0OO0O0OO000O ])#line:651
            OOOO00O000OOOOOO0 .append (O0OOOO00O000OOO00 )#line:652
            OOOO000OO000OO0OO =OOOO0OOO0OOOO00OO ._bitcount (OO00000O00000O000 ['cond']&OOO000O000000O00O [OOOOO0OO0O0OO000O ])#line:655
            O000000OO0O0O0OO0 .append (OOOO000OO000OO0OO )#line:656
        if (O00OO0O0OO0O0OO00 &sum (OOOO00O000OOOOOO0 )>0 ):#line:658
            for OOOOO0OO0O0OO000O in range (len (OOO000O000000O00O )):#line:659
                if O000000OO0O0O0OO0 [OOOOO0OO0O0OO000O ]>0 :#line:660
                    if OOOO00O000OOOOOO0 [OOOOO0OO0O0OO000O ]/sum (OOOO00O000OOOOOO0 )>O000000OO0O0O0OO0 [OOOOO0OO0O0OO000O ]/sum (O000000OO0O0O0OO0 ):#line:662
                        OO0OO00OO00O00OOO +=OOO0OOO0OO00O0OOO [OOOOO0OO0O0OO000O ]*((OOOO00O000OOOOOO0 [OOOOO0OO0O0OO000O ]/sum (OOOO00O000OOOOOO0 ))/(O000000OO0O0O0OO0 [OOOOO0OO0O0OO000O ]/sum (O000000OO0O0O0OO0 ))-1 )#line:663
        OOO00000O00OO00O0 =True #line:666
        for OO0O0O00OOO00O00O in OOOO0OOO0OOOO00OO .quantifiers .keys ():#line:667
            if OO0O0O00OOO00O00O .upper ()=='BASE':#line:668
                OOO00000O00OO00O0 =OOO00000O00OO00O0 and (OOOO0OOO0OOOO00OO .quantifiers .get (OO0O0O00OOO00O00O )<=O0000O0OO000O000O )#line:669
            if OO0O0O00OOO00O00O .upper ()=='RELBASE':#line:670
                OOO00000O00OO00O0 =OOO00000O00OO00O0 and (OOOO0OOO0OOOO00OO .quantifiers .get (OO0O0O00OOO00O00O )<=O0000O0OO000O000O *1.0 /OOOO0OOO0OOOO00OO .data ["rows_count"])#line:671
            if OO0O0O00OOO00O00O .upper ()=='AAD_SCORE':#line:672
                OOO00000O00OO00O0 =OOO00000O00OO00O0 and (OOOO0OOO0OOOO00OO .quantifiers .get (OO0O0O00OOO00O00O )<=OO0OO00OO00O00OOO )#line:673
        OOOOO0O00OOO0O000 ={}#line:675
        if OOO00000O00OO00O0 ==True :#line:676
            OOOO0OOO0OOOO00OO .stats ['total_valid']+=1 #line:678
            OOOOO0O00OOO0O000 ["base"]=O0000O0OO000O000O #line:679
            OOOOO0O00OOO0O000 ["rel_base"]=O0000O0OO000O000O *1.0 /OOOO0OOO0OOOO00OO .data ["rows_count"]#line:680
            OOOOO0O00OOO0O000 ["hist"]=OOOO00O000OOOOOO0 #line:681
            OOOOO0O00OOO0O000 ["aad_score"]=OO0OO00OO00O00OOO #line:683
            OOOOO0O00OOO0O000 ["hist_cond"]=O000000OO0O0O0OO0 #line:684
            OOOOO0O00OOO0O000 ["rel_hist"]=[OOO000O00OO000000 /sum (OOOO00O000OOOOOO0 )for OOO000O00OO000000 in OOOO00O000OOOOOO0 ]#line:685
            OOOOO0O00OOO0O000 ["rel_hist_cond"]=[OO0OO0O0OO0000O00 /sum (O000000OO0O0O0OO0 )for OO0OO0O0OO0000O00 in O000000OO0O0O0OO0 ]#line:686
        return OOO00000O00OO00O0 ,OOOOO0O00OOO0O000 #line:688
    def _verify4ft (O0O00O00O0OO0OO00 ,_OO00000O0000000OO ):#line:690
        O00O0000OO00O00OO ={}#line:691
        O00OO00O0O00O0OO0 =0 #line:692
        for OO00O0OO00OOOO0OO in O0O00O00O0OO0OO00 .task_actinfo ['cedents']:#line:693
            O00O0000OO00O00OO [OO00O0OO00OOOO0OO ['cedent_type']]=OO00O0OO00OOOO0OO ['filter_value']#line:695
            O00OO00O0O00O0OO0 =O00OO00O0O00O0OO0 +1 #line:696
        OOOO00000O0O0O0OO =O0O00O00O0OO0OO00 ._bitcount (O00O0000OO00O00OO ['ante']&O00O0000OO00O00OO ['succ']&O00O0000OO00O00OO ['cond'])#line:698
        O0OO0O00000O00O0O =None #line:699
        O0OO0O00000O00O0O =0 #line:700
        if OOOO00000O0O0O0OO >0 :#line:709
            O0OO0O00000O00O0O =O0O00O00O0OO0OO00 ._bitcount (O00O0000OO00O00OO ['ante']&O00O0000OO00O00OO ['succ']&O00O0000OO00O00OO ['cond'])*1.0 /O0O00O00O0OO0OO00 ._bitcount (O00O0000OO00O00OO ['ante']&O00O0000OO00O00OO ['cond'])#line:710
        O0OOO000O00O0OO00 =1 <<O0O00O00O0OO0OO00 .data ["rows_count"]#line:712
        O0OO00O0O0OO00O0O =O0O00O00O0OO0OO00 ._bitcount (O00O0000OO00O00OO ['ante']&O00O0000OO00O00OO ['succ']&O00O0000OO00O00OO ['cond'])#line:713
        OOO00OO00O000O0O0 =O0O00O00O0OO0OO00 ._bitcount (O00O0000OO00O00OO ['ante']&~(O0OOO000O00O0OO00 |O00O0000OO00O00OO ['succ'])&O00O0000OO00O00OO ['cond'])#line:714
        OO00O0OO00OOOO0OO =O0O00O00O0OO0OO00 ._bitcount (~(O0OOO000O00O0OO00 |O00O0000OO00O00OO ['ante'])&O00O0000OO00O00OO ['succ']&O00O0000OO00O00OO ['cond'])#line:715
        O000OOOOO0OO0O000 =O0O00O00O0OO0OO00 ._bitcount (~(O0OOO000O00O0OO00 |O00O0000OO00O00OO ['ante'])&~(O0OOO000O00O0OO00 |O00O0000OO00O00OO ['succ'])&O00O0000OO00O00OO ['cond'])#line:716
        OO0000O0O00OO00OO =0 #line:717
        if (O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 )*(O0OO00O0O0OO00O0O +OO00O0OO00OOOO0OO )>0 :#line:718
            OO0000O0O00OO00OO =O0OO00O0O0OO00O0O *(O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 +OO00O0OO00OOOO0OO +O000OOOOO0OO0O000 )/(O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 )/(O0OO00O0O0OO00O0O +OO00O0OO00OOOO0OO )-1 #line:719
        else :#line:720
            OO0000O0O00OO00OO =None #line:721
        OO000OO0000O00000 =0 #line:722
        if (O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 )*(O0OO00O0O0OO00O0O +OO00O0OO00OOOO0OO )>0 :#line:723
            OO000OO0000O00000 =1 -O0OO00O0O0OO00O0O *(O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 +OO00O0OO00OOOO0OO +O000OOOOO0OO0O000 )/(O0OO00O0O0OO00O0O +OOO00OO00O000O0O0 )/(O0OO00O0O0OO00O0O +OO00O0OO00OOOO0OO )#line:724
        else :#line:725
            OO000OO0000O00000 =None #line:726
        OOO0OO0O0OO0000O0 =True #line:727
        for O0O0000OO00OO000O in O0O00O00O0OO0OO00 .quantifiers .keys ():#line:728
            if O0O0000OO00OO000O .upper ()=='BASE':#line:729
                OOO0OO0O0OO0000O0 =OOO0OO0O0OO0000O0 and (O0O00O00O0OO0OO00 .quantifiers .get (O0O0000OO00OO000O )<=OOOO00000O0O0O0OO )#line:730
            if O0O0000OO00OO000O .upper ()=='RELBASE':#line:731
                OOO0OO0O0OO0000O0 =OOO0OO0O0OO0000O0 and (O0O00O00O0OO0OO00 .quantifiers .get (O0O0000OO00OO000O )<=OOOO00000O0O0O0OO *1.0 /O0O00O00O0OO0OO00 .data ["rows_count"])#line:732
            if (O0O0000OO00OO000O .upper ()=='PIM')or (O0O0000OO00OO000O .upper ()=='CONF'):#line:733
                OOO0OO0O0OO0000O0 =OOO0OO0O0OO0000O0 and (O0O00O00O0OO0OO00 .quantifiers .get (O0O0000OO00OO000O )<=O0OO0O00000O00O0O )#line:734
            if O0O0000OO00OO000O .upper ()=='AAD':#line:735
                if OO0000O0O00OO00OO !=None :#line:736
                    OOO0OO0O0OO0000O0 =OOO0OO0O0OO0000O0 and (O0O00O00O0OO0OO00 .quantifiers .get (O0O0000OO00OO000O )<=OO0000O0O00OO00OO )#line:737
                else :#line:738
                    OOO0OO0O0OO0000O0 =False #line:739
            if O0O0000OO00OO000O .upper ()=='BAD':#line:740
                if OO000OO0000O00000 !=None :#line:741
                    OOO0OO0O0OO0000O0 =OOO0OO0O0OO0000O0 and (O0O00O00O0OO0OO00 .quantifiers .get (O0O0000OO00OO000O )<=OO000OO0000O00000 )#line:742
                else :#line:743
                    OOO0OO0O0OO0000O0 =False #line:744
            OO0OO0OOO0OOO0000 ={}#line:745
        if OOO0OO0O0OO0000O0 ==True :#line:746
            O0O00O00O0OO0OO00 .stats ['total_valid']+=1 #line:748
            OO0OO0OOO0OOO0000 ["base"]=OOOO00000O0O0O0OO #line:749
            OO0OO0OOO0OOO0000 ["rel_base"]=OOOO00000O0O0O0OO *1.0 /O0O00O00O0OO0OO00 .data ["rows_count"]#line:750
            OO0OO0OOO0OOO0000 ["conf"]=O0OO0O00000O00O0O #line:751
            OO0OO0OOO0OOO0000 ["aad"]=OO0000O0O00OO00OO #line:752
            OO0OO0OOO0OOO0000 ["bad"]=OO000OO0000O00000 #line:753
            OO0OO0OOO0OOO0000 ["fourfold"]=[O0OO00O0O0OO00O0O ,OOO00OO00O000O0O0 ,OO00O0OO00OOOO0OO ,O000OOOOO0OO0O000 ]#line:754
        return OOO0OO0O0OO0000O0 ,OO0OO0OOO0OOO0000 #line:758
    def _verifysd4ft (O0OO0OOO0OO00000O ,_OOO0O0OOOO0000000 ):#line:760
        OOOOO0000OO00O0O0 ={}#line:761
        O00OOO0000OOO0000 =0 #line:762
        for O0O00OO00O000O000 in O0OO0OOO0OO00000O .task_actinfo ['cedents']:#line:763
            OOOOO0000OO00O0O0 [O0O00OO00O000O000 ['cedent_type']]=O0O00OO00O000O000 ['filter_value']#line:765
            O00OOO0000OOO0000 =O00OOO0000OOO0000 +1 #line:766
        O0OOOO000OO0O00O0 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:768
        O0O0O00O0OOOOOO00 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:769
        OO00OOO0OOO00OO00 =None #line:770
        OO0OOOO00OOO00O0O =0 #line:771
        O00OOO00000OO0OO0 =0 #line:772
        if O0OOOO000OO0O00O0 >0 :#line:781
            OO0OOOO00OOO00O0O =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])*1.0 /O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:782
        if O0O0O00O0OOOOOO00 >0 :#line:783
            O00OOO00000OO0OO0 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])*1.0 /O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:784
        OO0OO00OO00O0OOO0 =1 <<O0OO0OOO0OO00000O .data ["rows_count"]#line:786
        O000OO0O000O0OO00 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:787
        OO0O0O00OOO0O00OO =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['succ'])&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:788
        OOO0O000OO00OO0O0 =O0OO0OOO0OO00000O ._bitcount (~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['ante'])&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:789
        OOO0OOOOOOO0O000O =O0OO0OOO0OO00000O ._bitcount (~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['ante'])&~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['succ'])&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['frst'])#line:790
        O000O0O00OO000000 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:791
        O0O000O0O0OOOO0O0 =O0OO0OOO0OO00000O ._bitcount (OOOOO0000OO00O0O0 ['ante']&~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['succ'])&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:792
        OO0O0OO00OOO00OO0 =O0OO0OOO0OO00000O ._bitcount (~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['ante'])&OOOOO0000OO00O0O0 ['succ']&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:793
        O0O0OO0OO00O000OO =O0OO0OOO0OO00000O ._bitcount (~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['ante'])&~(OO0OO00OO00O0OOO0 |OOOOO0000OO00O0O0 ['succ'])&OOOOO0000OO00O0O0 ['cond']&OOOOO0000OO00O0O0 ['scnd'])#line:794
        OOO00OO000000O000 =True #line:795
        for O0OO0OO00OOOO00OO in O0OO0OOO0OO00000O .quantifiers .keys ():#line:796
            if (O0OO0OO00OOOO00OO .upper ()=='FRSTBASE')|(O0OO0OO00OOOO00OO .upper ()=='BASE1'):#line:797
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=O0OOOO000OO0O00O0 )#line:798
            if (O0OO0OO00OOOO00OO .upper ()=='SCNDBASE')|(O0OO0OO00OOOO00OO .upper ()=='BASE2'):#line:799
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=O0O0O00O0OOOOOO00 )#line:800
            if (O0OO0OO00OOOO00OO .upper ()=='FRSTRELBASE')|(O0OO0OO00OOOO00OO .upper ()=='RELBASE1'):#line:801
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=O0OOOO000OO0O00O0 *1.0 /O0OO0OOO0OO00000O .data ["rows_count"])#line:802
            if (O0OO0OO00OOOO00OO .upper ()=='SCNDRELBASE')|(O0OO0OO00OOOO00OO .upper ()=='RELBASE2'):#line:803
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=O0O0O00O0OOOOOO00 *1.0 /O0OO0OOO0OO00000O .data ["rows_count"])#line:804
            if (O0OO0OO00OOOO00OO .upper ()=='FRSTPIM')|(O0OO0OO00OOOO00OO .upper ()=='PIM1')|(O0OO0OO00OOOO00OO .upper ()=='FRSTCONF')|(O0OO0OO00OOOO00OO .upper ()=='CONF1'):#line:805
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=OO0OOOO00OOO00O0O )#line:806
            if (O0OO0OO00OOOO00OO .upper ()=='SCNDPIM')|(O0OO0OO00OOOO00OO .upper ()=='PIM2')|(O0OO0OO00OOOO00OO .upper ()=='SCNDCONF')|(O0OO0OO00OOOO00OO .upper ()=='CONF2'):#line:807
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=O00OOO00000OO0OO0 )#line:808
            if (O0OO0OO00OOOO00OO .upper ()=='DELTAPIM')|(O0OO0OO00OOOO00OO .upper ()=='DELTACONF'):#line:809
                OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=OO0OOOO00OOO00O0O -O00OOO00000OO0OO0 )#line:810
            if (O0OO0OO00OOOO00OO .upper ()=='RATIOPIM')|(O0OO0OO00OOOO00OO .upper ()=='RATIOCONF'):#line:813
                if (O00OOO00000OO0OO0 >0 ):#line:814
                    OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )<=OO0OOOO00OOO00O0O *1.0 /O00OOO00000OO0OO0 )#line:815
                else :#line:816
                    OOO00OO000000O000 =False #line:817
            if (O0OO0OO00OOOO00OO .upper ()=='RATIOPIM_LEQ')|(O0OO0OO00OOOO00OO .upper ()=='RATIOCONF_LEQ'):#line:818
                if (O00OOO00000OO0OO0 >0 ):#line:819
                    OOO00OO000000O000 =OOO00OO000000O000 and (O0OO0OOO0OO00000O .quantifiers .get (O0OO0OO00OOOO00OO )>=OO0OOOO00OOO00O0O *1.0 /O00OOO00000OO0OO0 )#line:820
                else :#line:821
                    OOO00OO000000O000 =False #line:822
        O0000OOO00OO000OO ={}#line:823
        if OOO00OO000000O000 ==True :#line:824
            O0OO0OOO0OO00000O .stats ['total_valid']+=1 #line:826
            O0000OOO00OO000OO ["base1"]=O0OOOO000OO0O00O0 #line:827
            O0000OOO00OO000OO ["base2"]=O0O0O00O0OOOOOO00 #line:828
            O0000OOO00OO000OO ["rel_base1"]=O0OOOO000OO0O00O0 *1.0 /O0OO0OOO0OO00000O .data ["rows_count"]#line:829
            O0000OOO00OO000OO ["rel_base2"]=O0O0O00O0OOOOOO00 *1.0 /O0OO0OOO0OO00000O .data ["rows_count"]#line:830
            O0000OOO00OO000OO ["conf1"]=OO0OOOO00OOO00O0O #line:831
            O0000OOO00OO000OO ["conf2"]=O00OOO00000OO0OO0 #line:832
            O0000OOO00OO000OO ["deltaconf"]=OO0OOOO00OOO00O0O -O00OOO00000OO0OO0 #line:833
            if (O00OOO00000OO0OO0 >0 ):#line:834
                O0000OOO00OO000OO ["ratioconf"]=OO0OOOO00OOO00O0O *1.0 /O00OOO00000OO0OO0 #line:835
            else :#line:836
                O0000OOO00OO000OO ["ratioconf"]=None #line:837
            O0000OOO00OO000OO ["fourfold1"]=[O000OO0O000O0OO00 ,OO0O0O00OOO0O00OO ,OOO0O000OO00OO0O0 ,OOO0OOOOOOO0O000O ]#line:838
            O0000OOO00OO000OO ["fourfold2"]=[O000O0O00OO000000 ,O0O000O0O0OOOO0O0 ,OO0O0OO00OOO00OO0 ,O0O0OO0OO00O000OO ]#line:839
        return OOO00OO000000O000 ,O0000OOO00OO000OO #line:843
    def _verifynewact4ft (O00O0000O0OO0O0O0 ,_OOOO00OO0000OO0OO ):#line:845
        OOOO0O0OOOOO00OO0 ={}#line:846
        for O0O00OO0O00O00O0O in O00O0000O0OO0O0O0 .task_actinfo ['cedents']:#line:847
            OOOO0O0OOOOO00OO0 [O0O00OO0O00O00O0O ['cedent_type']]=O0O00OO0O00O00O0O ['filter_value']#line:849
        O0000OOO0O0OO0OOO =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond'])#line:851
        OO00O0OOO00O000OO =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond']&OOOO0O0OOOOO00OO0 ['antv']&OOOO0O0OOOOO00OO0 ['sucv'])#line:852
        O0OOOO0O0O0OO0000 =None #line:853
        OOO0000O0O0OOOOOO =0 #line:854
        OOOO000OO0000OOO0 =0 #line:855
        if O0000OOO0O0OO0OOO >0 :#line:864
            OOO0000O0O0OOOOOO =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond'])*1.0 /O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['cond'])#line:865
        if OO00O0OOO00O000OO >0 :#line:866
            OOOO000OO0000OOO0 =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond']&OOOO0O0OOOOO00OO0 ['antv']&OOOO0O0OOOOO00OO0 ['sucv'])*1.0 /O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['cond']&OOOO0O0OOOOO00OO0 ['antv'])#line:868
        OO000OOOOO000O0OO =1 <<O00O0000O0OO0O0O0 .rows_count #line:870
        OO00O00000O0000OO =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond'])#line:871
        OO000OOO0O0O00OO0 =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&~(OO000OOOOO000O0OO |OOOO0O0OOOOO00OO0 ['succ'])&OOOO0O0OOOOO00OO0 ['cond'])#line:872
        OO0OOO0O0OO0OO0OO =O00O0000O0OO0O0O0 ._bitcount (~(OO000OOOOO000O0OO |OOOO0O0OOOOO00OO0 ['ante'])&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond'])#line:873
        O0OOO0O0OO000OOO0 =O00O0000O0OO0O0O0 ._bitcount (~(OO000OOOOO000O0OO |OOOO0O0OOOOO00OO0 ['ante'])&~(OO000OOOOO000O0OO |OOOO0O0OOOOO00OO0 ['succ'])&OOOO0O0OOOOO00OO0 ['cond'])#line:874
        OO00OO0OOO00000O0 =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond']&OOOO0O0OOOOO00OO0 ['antv']&OOOO0O0OOOOO00OO0 ['sucv'])#line:875
        OO0O0O0O000000000 =O00O0000O0OO0O0O0 ._bitcount (OOOO0O0OOOOO00OO0 ['ante']&~(OO000OOOOO000O0OO |(OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['sucv']))&OOOO0O0OOOOO00OO0 ['cond'])#line:876
        OOOO00O00O00OO00O =O00O0000O0OO0O0O0 ._bitcount (~(OO000OOOOO000O0OO |(OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['antv']))&OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['cond']&OOOO0O0OOOOO00OO0 ['sucv'])#line:877
        O00O0000O0OO000O0 =O00O0000O0OO0O0O0 ._bitcount (~(OO000OOOOO000O0OO |(OOOO0O0OOOOO00OO0 ['ante']&OOOO0O0OOOOO00OO0 ['antv']))&~(OO000OOOOO000O0OO |(OOOO0O0OOOOO00OO0 ['succ']&OOOO0O0OOOOO00OO0 ['sucv']))&OOOO0O0OOOOO00OO0 ['cond'])#line:878
        OO00O0O0OOO000O0O =True #line:879
        for O0O00O0O0O0OO00OO in O00O0000O0OO0O0O0 .quantifiers .keys ():#line:880
            if (O0O00O0O0O0OO00OO =='PreBase')|(O0O00O0O0O0OO00OO =='Base1'):#line:881
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=O0000OOO0O0OO0OOO )#line:882
            if (O0O00O0O0O0OO00OO =='PostBase')|(O0O00O0O0O0OO00OO =='Base2'):#line:883
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OO00O0OOO00O000OO )#line:884
            if (O0O00O0O0O0OO00OO =='PreRelBase')|(O0O00O0O0O0OO00OO =='RelBase1'):#line:885
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=O0000OOO0O0OO0OOO *1.0 /O00O0000O0OO0O0O0 .data ["rows_count"])#line:886
            if (O0O00O0O0O0OO00OO =='PostRelBase')|(O0O00O0O0O0OO00OO =='RelBase2'):#line:887
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OO00O0OOO00O000OO *1.0 /O00O0000O0OO0O0O0 .data ["rows_count"])#line:888
            if (O0O00O0O0O0OO00OO =='Prepim')|(O0O00O0O0O0OO00OO =='pim1')|(O0O00O0O0O0OO00OO =='PreConf')|(O0O00O0O0O0OO00OO =='conf1'):#line:889
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OOO0000O0O0OOOOOO )#line:890
            if (O0O00O0O0O0OO00OO =='Postpim')|(O0O00O0O0O0OO00OO =='pim2')|(O0O00O0O0O0OO00OO =='PostConf')|(O0O00O0O0O0OO00OO =='conf2'):#line:891
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OOOO000OO0000OOO0 )#line:892
            if (O0O00O0O0O0OO00OO =='Deltapim')|(O0O00O0O0O0OO00OO =='DeltaConf'):#line:893
                OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OOO0000O0O0OOOOOO -OOOO000OO0000OOO0 )#line:894
            if (O0O00O0O0O0OO00OO =='Ratiopim')|(O0O00O0O0O0OO00OO =='RatioConf'):#line:897
                if (OOOO000OO0000OOO0 >0 ):#line:898
                    OO00O0O0OOO000O0O =OO00O0O0OOO000O0O and (O00O0000O0OO0O0O0 .quantifiers .get (O0O00O0O0O0OO00OO )<=OOO0000O0O0OOOOOO *1.0 /OOOO000OO0000OOO0 )#line:899
                else :#line:900
                    OO00O0O0OOO000O0O =False #line:901
        OO00O00OO0OOO000O ={}#line:902
        if OO00O0O0OOO000O0O ==True :#line:903
            O00O0000O0OO0O0O0 .stats ['total_valid']+=1 #line:905
            OO00O00OO0OOO000O ["base1"]=O0000OOO0O0OO0OOO #line:906
            OO00O00OO0OOO000O ["base2"]=OO00O0OOO00O000OO #line:907
            OO00O00OO0OOO000O ["rel_base1"]=O0000OOO0O0OO0OOO *1.0 /O00O0000O0OO0O0O0 .data ["rows_count"]#line:908
            OO00O00OO0OOO000O ["rel_base2"]=OO00O0OOO00O000OO *1.0 /O00O0000O0OO0O0O0 .data ["rows_count"]#line:909
            OO00O00OO0OOO000O ["conf1"]=OOO0000O0O0OOOOOO #line:910
            OO00O00OO0OOO000O ["conf2"]=OOOO000OO0000OOO0 #line:911
            OO00O00OO0OOO000O ["deltaconf"]=OOO0000O0O0OOOOOO -OOOO000OO0000OOO0 #line:912
            if (OOOO000OO0000OOO0 >0 ):#line:913
                OO00O00OO0OOO000O ["ratioconf"]=OOO0000O0O0OOOOOO *1.0 /OOOO000OO0000OOO0 #line:914
            else :#line:915
                OO00O00OO0OOO000O ["ratioconf"]=None #line:916
            OO00O00OO0OOO000O ["fourfoldpre"]=[OO00O00000O0000OO ,OO000OOO0O0O00OO0 ,OO0OOO0O0OO0OO0OO ,O0OOO0O0OO000OOO0 ]#line:917
            OO00O00OO0OOO000O ["fourfoldpost"]=[OO00OO0OOO00000O0 ,OO0O0O0O000000000 ,OOOO00O00O00OO00O ,O00O0000O0OO000O0 ]#line:918
        return OO00O0O0OOO000O0O ,OO00O00OO0OOO000O #line:920
    def _verifyact4ft (OO0O00O00OOOO000O ,_O0O0O0OOO0OO0O0OO ):#line:922
        O0O000O0OO000O0OO ={}#line:923
        for O00O0O0OOOO0000OO in OO0O00O00OOOO000O .task_actinfo ['cedents']:#line:924
            O0O000O0OO000O0OO [O00O0O0OOOO0000OO ['cedent_type']]=O00O0O0OOOO0000OO ['filter_value']#line:926
        OOO0O0OOOO0OOO00O =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv-']&O0O000O0OO000O0OO ['sucv-'])#line:928
        OOO00000000000000 =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv+']&O0O000O0OO000O0OO ['sucv+'])#line:929
        O00O0000OO00O0O00 =None #line:930
        OO0000OOO0O0O00O0 =0 #line:931
        OO000OO0O00OO0O00 =0 #line:932
        if OOO0O0OOOO0OOO00O >0 :#line:941
            OO0000OOO0O0O00O0 =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv-']&O0O000O0OO000O0OO ['sucv-'])*1.0 /OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv-'])#line:943
        if OOO00000000000000 >0 :#line:944
            OO000OO0O00OO0O00 =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv+']&O0O000O0OO000O0OO ['sucv+'])*1.0 /OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv+'])#line:946
        O0O0000O00O00O00O =1 <<OO0O00O00OOOO000O .data ["rows_count"]#line:948
        O00OOOO0OO0O0OOO0 =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv-']&O0O000O0OO000O0OO ['sucv-'])#line:949
        O0OOOO0OO0OOOO00O =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv-']&~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['sucv-']))&O0O000O0OO000O0OO ['cond'])#line:950
        O00000OO0000OO0O0 =OO0O00O00OOOO000O ._bitcount (~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv-']))&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['sucv-'])#line:951
        O0OO0OO000000OO0O =OO0O00O00OOOO000O ._bitcount (~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv-']))&~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['sucv-']))&O0O000O0OO000O0OO ['cond'])#line:952
        OO0OOOO00O0OO00O0 =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['antv+']&O0O000O0OO000O0OO ['sucv+'])#line:953
        O0OO00O00O00OO00O =OO0O00O00OOOO000O ._bitcount (O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv+']&~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['sucv+']))&O0O000O0OO000O0OO ['cond'])#line:954
        O000O00O0OO0O00OO =OO0O00O00OOOO000O ._bitcount (~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv+']))&O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['cond']&O0O000O0OO000O0OO ['sucv+'])#line:955
        O000OO0OO0OO00O00 =OO0O00O00OOOO000O ._bitcount (~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['ante']&O0O000O0OO000O0OO ['antv+']))&~(O0O0000O00O00O00O |(O0O000O0OO000O0OO ['succ']&O0O000O0OO000O0OO ['sucv+']))&O0O000O0OO000O0OO ['cond'])#line:956
        OOOOOO00O00OO000O =True #line:957
        for O00O0OO0OO000O000 in OO0O00O00OOOO000O .quantifiers .keys ():#line:958
            if (O00O0OO0OO000O000 =='PreBase')|(O00O0OO0OO000O000 =='Base1'):#line:959
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OOO0O0OOOO0OOO00O )#line:960
            if (O00O0OO0OO000O000 =='PostBase')|(O00O0OO0OO000O000 =='Base2'):#line:961
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OOO00000000000000 )#line:962
            if (O00O0OO0OO000O000 =='PreRelBase')|(O00O0OO0OO000O000 =='RelBase1'):#line:963
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OOO0O0OOOO0OOO00O *1.0 /OO0O00O00OOOO000O .data ["rows_count"])#line:964
            if (O00O0OO0OO000O000 =='PostRelBase')|(O00O0OO0OO000O000 =='RelBase2'):#line:965
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OOO00000000000000 *1.0 /OO0O00O00OOOO000O .data ["rows_count"])#line:966
            if (O00O0OO0OO000O000 =='Prepim')|(O00O0OO0OO000O000 =='pim1')|(O00O0OO0OO000O000 =='PreConf')|(O00O0OO0OO000O000 =='conf1'):#line:967
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OO0000OOO0O0O00O0 )#line:968
            if (O00O0OO0OO000O000 =='Postpim')|(O00O0OO0OO000O000 =='pim2')|(O00O0OO0OO000O000 =='PostConf')|(O00O0OO0OO000O000 =='conf2'):#line:969
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OO000OO0O00OO0O00 )#line:970
            if (O00O0OO0OO000O000 =='Deltapim')|(O00O0OO0OO000O000 =='DeltaConf'):#line:971
                OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OO0000OOO0O0O00O0 -OO000OO0O00OO0O00 )#line:972
            if (O00O0OO0OO000O000 =='Ratiopim')|(O00O0OO0OO000O000 =='RatioConf'):#line:975
                if (OO0000OOO0O0O00O0 >0 ):#line:976
                    OOOOOO00O00OO000O =OOOOOO00O00OO000O and (OO0O00O00OOOO000O .quantifiers .get (O00O0OO0OO000O000 )<=OO000OO0O00OO0O00 *1.0 /OO0000OOO0O0O00O0 )#line:977
                else :#line:978
                    OOOOOO00O00OO000O =False #line:979
        O00O00OOOOOOO0O00 ={}#line:980
        if OOOOOO00O00OO000O ==True :#line:981
            OO0O00O00OOOO000O .stats ['total_valid']+=1 #line:983
            O00O00OOOOOOO0O00 ["base1"]=OOO0O0OOOO0OOO00O #line:984
            O00O00OOOOOOO0O00 ["base2"]=OOO00000000000000 #line:985
            O00O00OOOOOOO0O00 ["rel_base1"]=OOO0O0OOOO0OOO00O *1.0 /OO0O00O00OOOO000O .data ["rows_count"]#line:986
            O00O00OOOOOOO0O00 ["rel_base2"]=OOO00000000000000 *1.0 /OO0O00O00OOOO000O .data ["rows_count"]#line:987
            O00O00OOOOOOO0O00 ["conf1"]=OO0000OOO0O0O00O0 #line:988
            O00O00OOOOOOO0O00 ["conf2"]=OO000OO0O00OO0O00 #line:989
            O00O00OOOOOOO0O00 ["deltaconf"]=OO0000OOO0O0O00O0 -OO000OO0O00OO0O00 #line:990
            if (OO0000OOO0O0O00O0 >0 ):#line:991
                O00O00OOOOOOO0O00 ["ratioconf"]=OO000OO0O00OO0O00 *1.0 /OO0000OOO0O0O00O0 #line:992
            else :#line:993
                O00O00OOOOOOO0O00 ["ratioconf"]=None #line:994
            O00O00OOOOOOO0O00 ["fourfoldpre"]=[O00OOOO0OO0O0OOO0 ,O0OOOO0OO0OOOO00O ,O00000OO0000OO0O0 ,O0OO0OO000000OO0O ]#line:995
            O00O00OOOOOOO0O00 ["fourfoldpost"]=[OO0OOOO00O0OO00O0 ,O0OO00O00O00OO00O ,O000O00O0OO0O00OO ,O000OO0OO0OO00O00 ]#line:996
        return OOOOOO00O00OO000O ,O00O00OOOOOOO0O00 #line:998
    def _verify_opt (OOO00O00OOO00O0O0 ,OOO0O00OOOOO0O0O0 ,O000000OO0000O0OO ):#line:1000
        OOO00O00OOO00O0O0 .stats ['total_ver']+=1 #line:1001
        OO0O00O000OO0O000 =False #line:1002
        if not (OOO0O00OOOOO0O0O0 ['optim'].get ('only_con')):#line:1005
            return False #line:1006
        if not (OOO00O00OOO00O0O0 .options ['optimizations']):#line:1009
            return False #line:1011
        O0O00OO000O00O0OO ={}#line:1013
        for OO00OO0O0O0OO000O in OOO00O00OOO00O0O0 .task_actinfo ['cedents']:#line:1014
            O0O00OO000O00O0OO [OO00OO0O0O0OO000O ['cedent_type']]=OO00OO0O0O0OO000O ['filter_value']#line:1016
        O0O000O00O00O00O0 =1 <<OOO00O00OOO00O0O0 .data ["rows_count"]#line:1018
        OOOO0OOO00OO00OOO =O0O000O00O00O00O0 -1 #line:1019
        O000000000O0000OO =""#line:1020
        O00O0OOOOO0OO0OOO =0 #line:1021
        if (O0O00OO000O00O0OO .get ('ante')!=None ):#line:1022
            OOOO0OOO00OO00OOO =OOOO0OOO00OO00OOO &O0O00OO000O00O0OO ['ante']#line:1023
        if (O0O00OO000O00O0OO .get ('succ')!=None ):#line:1024
            OOOO0OOO00OO00OOO =OOOO0OOO00OO00OOO &O0O00OO000O00O0OO ['succ']#line:1025
        if (O0O00OO000O00O0OO .get ('cond')!=None ):#line:1026
            OOOO0OOO00OO00OOO =OOOO0OOO00OO00OOO &O0O00OO000O00O0OO ['cond']#line:1027
        OOOOO00OOO0O00O0O =None #line:1030
        if (OOO00O00OOO00O0O0 .proc =='CFMiner')|(OOO00O00OOO00O0O0 .proc =='4ftMiner')|(OOO00O00OOO00O0O0 .proc =='UICMiner'):#line:1055
            O0O000OO0OO0O00OO =OOO00O00OOO00O0O0 ._bitcount (OOOO0OOO00OO00OOO )#line:1056
            if not (OOO00O00OOO00O0O0 ._opt_base ==None ):#line:1057
                if not (OOO00O00OOO00O0O0 ._opt_base <=O0O000OO0OO0O00OO ):#line:1058
                    OO0O00O000OO0O000 =True #line:1059
            if not (OOO00O00OOO00O0O0 ._opt_relbase ==None ):#line:1061
                if not (OOO00O00OOO00O0O0 ._opt_relbase <=O0O000OO0OO0O00OO *1.0 /OOO00O00OOO00O0O0 .data ["rows_count"]):#line:1062
                    OO0O00O000OO0O000 =True #line:1063
        if (OOO00O00OOO00O0O0 .proc =='SD4ftMiner'):#line:1065
            O0O000OO0OO0O00OO =OOO00O00OOO00O0O0 ._bitcount (OOOO0OOO00OO00OOO )#line:1066
            if (not (OOO00O00OOO00O0O0 ._opt_base1 ==None ))&(not (OOO00O00OOO00O0O0 ._opt_base2 ==None )):#line:1067
                if not (max (OOO00O00OOO00O0O0 ._opt_base1 ,OOO00O00OOO00O0O0 ._opt_base2 )<=O0O000OO0OO0O00OO ):#line:1068
                    OO0O00O000OO0O000 =True #line:1070
            if (not (OOO00O00OOO00O0O0 ._opt_relbase1 ==None ))&(not (OOO00O00OOO00O0O0 ._opt_relbase2 ==None )):#line:1071
                if not (max (OOO00O00OOO00O0O0 ._opt_relbase1 ,OOO00O00OOO00O0O0 ._opt_relbase2 )<=O0O000OO0OO0O00OO *1.0 /OOO00O00OOO00O0O0 .data ["rows_count"]):#line:1072
                    OO0O00O000OO0O000 =True #line:1073
        return OO0O00O000OO0O000 #line:1075
        if OOO00O00OOO00O0O0 .proc =='CFMiner':#line:1078
            if (O000000OO0000O0OO ['cedent_type']=='cond')&(O000000OO0000O0OO ['defi'].get ('type')=='con'):#line:1079
                O0O000OO0OO0O00OO =bin (O0O00OO000O00O0OO ['cond']).count ("1")#line:1080
                O00OOOO0O0000OOO0 =True #line:1081
                for O000OOOO00O000OO0 in OOO00O00OOO00O0O0 .quantifiers .keys ():#line:1082
                    if O000OOOO00O000OO0 =='Base':#line:1083
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO )#line:1084
                        if not (O00OOOO0O0000OOO0 ):#line:1085
                            print (f"...optimization : base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1086
                    if O000OOOO00O000OO0 =='RelBase':#line:1087
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO *1.0 /OOO00O00OOO00O0O0 .data ["rows_count"])#line:1088
                        if not (O00OOOO0O0000OOO0 ):#line:1089
                            print (f"...optimization : base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1090
                OO0O00O000OO0O000 =not (O00OOOO0O0000OOO0 )#line:1091
        elif OOO00O00OOO00O0O0 .proc =='4ftMiner':#line:1092
            if (O000000OO0000O0OO ['cedent_type']=='cond')&(O000000OO0000O0OO ['defi'].get ('type')=='con'):#line:1093
                O0O000OO0OO0O00OO =bin (O0O00OO000O00O0OO ['cond']).count ("1")#line:1094
                O00OOOO0O0000OOO0 =True #line:1095
                for O000OOOO00O000OO0 in OOO00O00OOO00O0O0 .quantifiers .keys ():#line:1096
                    if O000OOOO00O000OO0 =='Base':#line:1097
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO )#line:1098
                        if not (O00OOOO0O0000OOO0 ):#line:1099
                            print (f"...optimization : base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1100
                    if O000OOOO00O000OO0 =='RelBase':#line:1101
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO *1.0 /OOO00O00OOO00O0O0 .data ["rows_count"])#line:1102
                        if not (O00OOOO0O0000OOO0 ):#line:1103
                            print (f"...optimization : base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1104
                OO0O00O000OO0O000 =not (O00OOOO0O0000OOO0 )#line:1105
            if (O000000OO0000O0OO ['cedent_type']=='ante')&(O000000OO0000O0OO ['defi'].get ('type')=='con'):#line:1106
                O0O000OO0OO0O00OO =bin (O0O00OO000O00O0OO ['ante']&O0O00OO000O00O0OO ['cond']).count ("1")#line:1107
                O00OOOO0O0000OOO0 =True #line:1108
                for O000OOOO00O000OO0 in OOO00O00OOO00O0O0 .quantifiers .keys ():#line:1109
                    if O000OOOO00O000OO0 =='Base':#line:1110
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO )#line:1111
                        if not (O00OOOO0O0000OOO0 ):#line:1112
                            print (f"...optimization : ANTE: base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1113
                    if O000OOOO00O000OO0 =='RelBase':#line:1114
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O000OO0OO0O00OO *1.0 /OOO00O00OOO00O0O0 .data ["rows_count"])#line:1115
                        if not (O00OOOO0O0000OOO0 ):#line:1116
                            print (f"...optimization : ANTE:  base is {O0O000OO0OO0O00OO} for {O000000OO0000O0OO['generated_string']}")#line:1117
                OO0O00O000OO0O000 =not (O00OOOO0O0000OOO0 )#line:1118
            if (O000000OO0000O0OO ['cedent_type']=='succ')&(O000000OO0000O0OO ['defi'].get ('type')=='con'):#line:1119
                O0O000OO0OO0O00OO =bin (O0O00OO000O00O0OO ['ante']&O0O00OO000O00O0OO ['cond']&O0O00OO000O00O0OO ['succ']).count ("1")#line:1120
                OOOOO00OOO0O00O0O =0 #line:1121
                if O0O000OO0OO0O00OO >0 :#line:1122
                    OOOOO00OOO0O00O0O =bin (O0O00OO000O00O0OO ['ante']&O0O00OO000O00O0OO ['succ']&O0O00OO000O00O0OO ['cond']).count ("1")*1.0 /bin (O0O00OO000O00O0OO ['ante']&O0O00OO000O00O0OO ['cond']).count ("1")#line:1123
                O0O000O00O00O00O0 =1 <<OOO00O00OOO00O0O0 .data ["rows_count"]#line:1124
                O0O00000OO0O00O0O =bin (O0O00OO000O00O0OO ['ante']&O0O00OO000O00O0OO ['succ']&O0O00OO000O00O0OO ['cond']).count ("1")#line:1125
                O0OOO0OO00000O0OO =bin (O0O00OO000O00O0OO ['ante']&~(O0O000O00O00O00O0 |O0O00OO000O00O0OO ['succ'])&O0O00OO000O00O0OO ['cond']).count ("1")#line:1126
                OO00OO0O0O0OO000O =bin (~(O0O000O00O00O00O0 |O0O00OO000O00O0OO ['ante'])&O0O00OO000O00O0OO ['succ']&O0O00OO000O00O0OO ['cond']).count ("1")#line:1127
                OOO0O0O000OO0O0OO =bin (~(O0O000O00O00O00O0 |O0O00OO000O00O0OO ['ante'])&~(O0O000O00O00O00O0 |O0O00OO000O00O0OO ['succ'])&O0O00OO000O00O0OO ['cond']).count ("1")#line:1128
                O00OOOO0O0000OOO0 =True #line:1129
                for O000OOOO00O000OO0 in OOO00O00OOO00O0O0 .quantifiers .keys ():#line:1130
                    if O000OOOO00O000OO0 =='pim':#line:1131
                        O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=OOOOO00OOO0O00O0O )#line:1132
                    if not (O00OOOO0O0000OOO0 ):#line:1133
                        print (f"...optimization : SUCC:  pim is {OOOOO00OOO0O00O0O} for {O000000OO0000O0OO['generated_string']}")#line:1134
                    if O000OOOO00O000OO0 =='aad':#line:1136
                        if (O0O00000OO0O00O0O +O0OOO0OO00000O0OO )*(O0O00000OO0O00O0O +OO00OO0O0O0OO000O )>0 :#line:1137
                            O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=O0O00000OO0O00O0O *(O0O00000OO0O00O0O +O0OOO0OO00000O0OO +OO00OO0O0O0OO000O +OOO0O0O000OO0O0OO )/(O0O00000OO0O00O0O +O0OOO0OO00000O0OO )/(O0O00000OO0O00O0O +OO00OO0O0O0OO000O )-1 )#line:1138
                        else :#line:1139
                            O00OOOO0O0000OOO0 =False #line:1140
                        if not (O00OOOO0O0000OOO0 ):#line:1141
                            O000O00OOO0O00000 =O0O00000OO0O00O0O *(O0O00000OO0O00O0O +O0OOO0OO00000O0OO +OO00OO0O0O0OO000O +OOO0O0O000OO0O0OO )/(O0O00000OO0O00O0O +O0OOO0OO00000O0OO )/(O0O00000OO0O00O0O +OO00OO0O0O0OO000O )-1 #line:1142
                            print (f"...optimization : SUCC:  aad is {O000O00OOO0O00000} for {O000000OO0000O0OO['generated_string']}")#line:1143
                    if O000OOOO00O000OO0 =='bad':#line:1144
                        if (O0O00000OO0O00O0O +O0OOO0OO00000O0OO )*(O0O00000OO0O00O0O +OO00OO0O0O0OO000O )>0 :#line:1145
                            O00OOOO0O0000OOO0 =O00OOOO0O0000OOO0 and (OOO00O00OOO00O0O0 .quantifiers .get (O000OOOO00O000OO0 )<=1 -O0O00000OO0O00O0O *(O0O00000OO0O00O0O +O0OOO0OO00000O0OO +OO00OO0O0O0OO000O +OOO0O0O000OO0O0OO )/(O0O00000OO0O00O0O +O0OOO0OO00000O0OO )/(O0O00000OO0O00O0O +OO00OO0O0O0OO000O ))#line:1146
                        else :#line:1147
                            O00OOOO0O0000OOO0 =False #line:1148
                        if not (O00OOOO0O0000OOO0 ):#line:1149
                            OO0OO0000O00O00O0 =1 -O0O00000OO0O00O0O *(O0O00000OO0O00O0O +O0OOO0OO00000O0OO +OO00OO0O0O0OO000O +OOO0O0O000OO0O0OO )/(O0O00000OO0O00O0O +O0OOO0OO00000O0OO )/(O0O00000OO0O00O0O +OO00OO0O0O0OO000O )#line:1150
                            print (f"...optimization : SUCC:  bad is {OO0OO0000O00O00O0} for {O000000OO0000O0OO['generated_string']}")#line:1151
                OO0O00O000OO0O000 =not (O00OOOO0O0000OOO0 )#line:1152
        if (OO0O00O000OO0O000 ):#line:1153
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O000000OO0000O0OO['cedent_type']}")#line:1154
        return OO0O00O000OO0O000 #line:1155
    def _print (OOO0OO00OOOOOOO00 ,OOO000O00OO0OOOOO ,_OOOO00OOOOO0000OO ,_O000OOO00O00OO0O0 ):#line:1158
        if (len (_OOOO00OOOOO0000OO ))!=len (_O000OOO00O00OO0O0 ):#line:1159
            print ("DIFF IN LEN for following cedent : "+str (len (_OOOO00OOOOO0000OO ))+" vs "+str (len (_O000OOO00O00OO0O0 )))#line:1160
            print ("trace cedent : "+str (_OOOO00OOOOO0000OO )+", traces "+str (_O000OOO00O00OO0O0 ))#line:1161
        OO0OO00O00000000O =''#line:1162
        O00000OO0OO00OO00 ={}#line:1163
        O000000OOO0OOOO0O =[]#line:1164
        for O0OO00OO0OO00O0OO in range (len (_OOOO00OOOOO0000OO )):#line:1165
            O0O00OO0OOO00O000 =OOO0OO00OOOOOOO00 .data ["varname"].index (OOO000O00OO0OOOOO ['defi'].get ('attributes')[_OOOO00OOOOO0000OO [O0OO00OO0OO00O0OO ]].get ('name'))#line:1166
            OO0OO00O00000000O =OO0OO00O00000000O +OOO0OO00OOOOOOO00 .data ["varname"][O0O00OO0OOO00O000 ]+'('#line:1168
            O000000OOO0OOOO0O .append (O0O00OO0OOO00O000 )#line:1169
            OOOOO0O0O0OO0OOOO =[]#line:1170
            for O00OOO00O0OOOOO0O in _O000OOO00O00OO0O0 [O0OO00OO0OO00O0OO ]:#line:1171
                OO0OO00O00000000O =OO0OO00O00000000O +str (OOO0OO00OOOOOOO00 .data ["catnames"][O0O00OO0OOO00O000 ][O00OOO00O0OOOOO0O ])+" "#line:1172
                OOOOO0O0O0OO0OOOO .append (str (OOO0OO00OOOOOOO00 .data ["catnames"][O0O00OO0OOO00O000 ][O00OOO00O0OOOOO0O ]))#line:1173
            OO0OO00O00000000O =OO0OO00O00000000O [:-1 ]+')'#line:1174
            O00000OO0OO00OO00 [OOO0OO00OOOOOOO00 .data ["varname"][O0O00OO0OOO00O000 ]]=OOOOO0O0O0OO0OOOO #line:1175
            if O0OO00OO0OO00O0OO +1 <len (_OOOO00OOOOO0000OO ):#line:1176
                OO0OO00O00000000O =OO0OO00O00000000O +' & '#line:1177
        return OO0OO00O00000000O ,O00000OO0OO00OO00 ,O000000OOO0OOOO0O #line:1181
    def _print_hypo (O00O00O0O0O0O0O0O ,O0OOO00O0OOOOO000 ):#line:1183
        O00O00O0O0O0O0O0O .print_rule (O0OOO00O0OOOOO000 )#line:1184
    def _print_rule (O0O00OO000O0OOOO0 ,O000OO0OO0O0OO0OO ):#line:1186
        if O0O00OO000O0OOOO0 .verbosity ['print_rules']:#line:1187
            print ('Rules info : '+str (O000OO0OO0O0OO0OO ['params']))#line:1188
            for OOOOOOO00OOO0000O in O0O00OO000O0OOOO0 .task_actinfo ['cedents']:#line:1189
                print (OOOOOOO00OOO0000O ['cedent_type']+' = '+OOOOOOO00OOO0000O ['generated_string'])#line:1190
    def _genvar (OO00O0O000000O0O0 ,OO00OO0OO000OO00O ,OOO0OOO0000O0O0OO ,_O0OOOOO00OO0O00O0 ,_O000O00O0OOOO000O ,_OOOOOOO0OO00OOOO0 ,_OOOO0O0OOOO0O0OOO ,_OOO0O0000O0000000 ,_O00O000OO00OO0O00 ,_O00000O00O0O00O00 ):#line:1192
        _O00O0OO00000O0000 =0 #line:1193
        if OOO0OOO0000O0O0OO ['num_cedent']>0 :#line:1194
            _O00O0OO00000O0000 =(_O00000O00O0O00O00 -_O00O000OO00OO0O00 )/OOO0OOO0000O0O0OO ['num_cedent']#line:1195
        for O0OO000OO0OO0000O in range (OOO0OOO0000O0O0OO ['num_cedent']):#line:1196
            if len (_O0OOOOO00OO0O00O0 )==0 or O0OO000OO0OO0000O >_O0OOOOO00OO0O00O0 [-1 ]:#line:1197
                _O0OOOOO00OO0O00O0 .append (O0OO000OO0OO0000O )#line:1198
                O00000OO000000O0O =OO00O0O000000O0O0 .data ["varname"].index (OOO0OOO0000O0O0OO ['defi'].get ('attributes')[O0OO000OO0OO0000O ].get ('name'))#line:1199
                _O0OOOO00OOO000O00 =OOO0OOO0000O0O0OO ['defi'].get ('attributes')[O0OO000OO0OO0000O ].get ('minlen')#line:1200
                _OOOO00O0O000OOOO0 =OOO0OOO0000O0O0OO ['defi'].get ('attributes')[O0OO000OO0OO0000O ].get ('maxlen')#line:1201
                _O0OOOO0O0O0000O00 =OOO0OOO0000O0O0OO ['defi'].get ('attributes')[O0OO000OO0OO0000O ].get ('type')#line:1202
                OO00000000OOOO000 =len (OO00O0O000000O0O0 .data ["dm"][O00000OO000000O0O ])#line:1203
                _O00OO0000O000000O =[]#line:1204
                _O000O00O0OOOO000O .append (_O00OO0000O000000O )#line:1205
                _O0OOO00OOO00000O0 =int (0 )#line:1206
                OO00O0O000000O0O0 ._gencomb (OO00OO0OO000OO00O ,OOO0OOO0000O0O0OO ,_O0OOOOO00OO0O00O0 ,_O000O00O0OOOO000O ,_O00OO0000O000000O ,_OOOOOOO0OO00OOOO0 ,_O0OOO00OOO00000O0 ,OO00000000OOOO000 ,_O0OOOO0O0O0000O00 ,_OOOO0O0OOOO0O0OOO ,_OOO0O0000O0000000 ,_O0OOOO00OOO000O00 ,_OOOO00O0O000OOOO0 ,_O00O000OO00OO0O00 +O0OO000OO0OO0000O *_O00O0OO00000O0000 ,_O00O000OO00OO0O00 +(O0OO000OO0OO0000O +1 )*_O00O0OO00000O0000 )#line:1207
                _O000O00O0OOOO000O .pop ()#line:1208
                _O0OOOOO00OO0O00O0 .pop ()#line:1209
    def _gencomb (O0OO00000000O0O0O ,OOOO00O0O000O0OOO ,OO0O0O0O00OO0OO0O ,_O0O00O0OOO0O0OO00 ,_O0O0O0000OOO0OOO0 ,_OOOOO00O00O000OO0 ,_O00OOO0OOOOOOOOO0 ,_OO0O0000O00O000OO ,OO0O00O0OO0O0OO0O ,_OO0OOO000OOOOOOO0 ,_O00000O0O0OO00O00 ,_OOOO0OO0O00OO000O ,_OO000O0OOO000O0O0 ,_O0000O0000O0O0OOO ,_OO0O00OOOOO00O000 ,_OO0OOOOOOOO0OOOO0 ):#line:1211
        _O00OO00OOOOOOO00O =[]#line:1212
        if _OO0OOO000OOOOOOO0 =="subset":#line:1213
            if len (_OOOOO00O00O000OO0 )==0 :#line:1214
                _O00OO00OOOOOOO00O =range (OO0O00O0OO0O0OO0O )#line:1215
            else :#line:1216
                _O00OO00OOOOOOO00O =range (_OOOOO00O00O000OO0 [-1 ]+1 ,OO0O00O0OO0O0OO0O )#line:1217
        elif _OO0OOO000OOOOOOO0 =="seq":#line:1218
            if len (_OOOOO00O00O000OO0 )==0 :#line:1219
                _O00OO00OOOOOOO00O =range (OO0O00O0OO0O0OO0O -_OO000O0OOO000O0O0 +1 )#line:1220
            else :#line:1221
                if _OOOOO00O00O000OO0 [-1 ]+1 ==OO0O00O0OO0O0OO0O :#line:1222
                    return #line:1223
                O0OO00O000O0O0O00 =_OOOOO00O00O000OO0 [-1 ]+1 #line:1224
                _O00OO00OOOOOOO00O .append (O0OO00O000O0O0O00 )#line:1225
        elif _OO0OOO000OOOOOOO0 =="lcut":#line:1226
            if len (_OOOOO00O00O000OO0 )==0 :#line:1227
                O0OO00O000O0O0O00 =0 ;#line:1228
            else :#line:1229
                if _OOOOO00O00O000OO0 [-1 ]+1 ==OO0O00O0OO0O0OO0O :#line:1230
                    return #line:1231
                O0OO00O000O0O0O00 =_OOOOO00O00O000OO0 [-1 ]+1 #line:1232
            _O00OO00OOOOOOO00O .append (O0OO00O000O0O0O00 )#line:1233
        elif _OO0OOO000OOOOOOO0 =="rcut":#line:1234
            if len (_OOOOO00O00O000OO0 )==0 :#line:1235
                O0OO00O000O0O0O00 =OO0O00O0OO0O0OO0O -1 ;#line:1236
            else :#line:1237
                if _OOOOO00O00O000OO0 [-1 ]==0 :#line:1238
                    return #line:1239
                O0OO00O000O0O0O00 =_OOOOO00O00O000OO0 [-1 ]-1 #line:1240
            _O00OO00OOOOOOO00O .append (O0OO00O000O0O0O00 )#line:1242
        elif _OO0OOO000OOOOOOO0 =="one":#line:1243
            if len (_OOOOO00O00O000OO0 )==0 :#line:1244
                O00OOO0O000OO0O00 =O0OO00000000O0O0O .data ["varname"].index (OO0O0O0O00OO0OO0O ['defi'].get ('attributes')[_O0O00O0OOO0O0OO00 [-1 ]].get ('name'))#line:1245
                try :#line:1246
                    O0OO00O000O0O0O00 =O0OO00000000O0O0O .data ["catnames"][O00OOO0O000OO0O00 ].index (OO0O0O0O00OO0OO0O ['defi'].get ('attributes')[_O0O00O0OOO0O0OO00 [-1 ]].get ('value'))#line:1247
                except :#line:1248
                    print (f"ERROR: attribute '{OO0O0O0O00OO0OO0O['defi'].get('attributes')[_O0O00O0OOO0O0OO00[-1]].get('name')}' has not value '{OO0O0O0O00OO0OO0O['defi'].get('attributes')[_O0O00O0OOO0O0OO00[-1]].get('value')}'")#line:1249
                    exit (1 )#line:1250
                _O00OO00OOOOOOO00O .append (O0OO00O000O0O0O00 )#line:1251
                _OO000O0OOO000O0O0 =1 #line:1252
                _O0000O0000O0O0OOO =1 #line:1253
            else :#line:1254
                print ("DEBUG: one category should not have more categories")#line:1255
                return #line:1256
        else :#line:1257
            print ("Attribute type "+_OO0OOO000OOOOOOO0 +" not supported.")#line:1258
            return #line:1259
        if len (_O00OO00OOOOOOO00O )>0 :#line:1261
            _O0O0OO0OO00O0OOO0 =(_OO0OOOOOOOO0OOOO0 -_OO0O00OOOOO00O000 )/len (_O00OO00OOOOOOO00O )#line:1262
        else :#line:1263
            _O0O0OO0OO00O0OOO0 =0 #line:1264
        _O00000O0O00O0O00O =0 #line:1266
        for O000O0OOOO000OO00 in _O00OO00OOOOOOO00O :#line:1268
                _OOOOO00O00O000OO0 .append (O000O0OOOO000OO00 )#line:1270
                _O0O0O0000OOO0OOO0 .pop ()#line:1271
                _O0O0O0000OOO0OOO0 .append (_OOOOO00O00O000OO0 )#line:1272
                _OO000O00O0OO00O00 =_OO0O0000O00O000OO |O0OO00000000O0O0O .data ["dm"][O0OO00000000O0O0O .data ["varname"].index (OO0O0O0O00OO0OO0O ['defi'].get ('attributes')[_O0O00O0OOO0O0OO00 [-1 ]].get ('name'))][O000O0OOOO000OO00 ]#line:1276
                _OOOO0O0000OOOO000 =1 #line:1278
                if (len (_O0O00O0OOO0O0OO00 )<_O00000O0O0OO00O00 ):#line:1279
                    _OOOO0O0000OOOO000 =-1 #line:1280
                if (len (_O0O0O0000OOO0OOO0 [-1 ])<_OO000O0OOO000O0O0 ):#line:1282
                    _OOOO0O0000OOOO000 =0 #line:1283
                _O0OOOO0O0OOO0O0OO =0 #line:1285
                if OO0O0O0O00OO0OO0O ['defi'].get ('type')=='con':#line:1286
                    _O0OOOO0O0OOO0O0OO =_O00OOO0OOOOOOOOO0 &_OO000O00O0OO00O00 #line:1287
                else :#line:1288
                    _O0OOOO0O0OOO0O0OO =_O00OOO0OOOOOOOOO0 |_OO000O00O0OO00O00 #line:1289
                OO0O0O0O00OO0OO0O ['trace_cedent']=_O0O00O0OOO0O0OO00 #line:1290
                OO0O0O0O00OO0OO0O ['traces']=_O0O0O0000OOO0OOO0 #line:1291
                O0O0O0000O00000OO ,OOOOOO0O0O0OOO0O0 ,O0OO000000OOO0OOO =O0OO00000000O0O0O ._print (OO0O0O0O00OO0OO0O ,_O0O00O0OOO0O0OO00 ,_O0O0O0000OOO0OOO0 )#line:1292
                OO0O0O0O00OO0OO0O ['generated_string']=O0O0O0000O00000OO #line:1293
                OO0O0O0O00OO0OO0O ['rule']=OOOOOO0O0O0OOO0O0 #line:1294
                OO0O0O0O00OO0OO0O ['filter_value']=_O0OOOO0O0OOO0O0OO #line:1295
                OO0O0O0O00OO0OO0O ['traces']=copy .deepcopy (_O0O0O0000OOO0OOO0 )#line:1296
                OO0O0O0O00OO0OO0O ['trace_cedent']=copy .deepcopy (_O0O00O0OOO0O0OO00 )#line:1297
                OO0O0O0O00OO0OO0O ['trace_cedent_asindata']=copy .deepcopy (O0OO000000OOO0OOO )#line:1298
                OOOO00O0O000O0OOO ['cedents'].append (OO0O0O0O00OO0OO0O )#line:1300
                O0000O00O0OO0OO0O =O0OO00000000O0O0O ._verify_opt (OOOO00O0O000O0OOO ,OO0O0O0O00OO0OO0O )#line:1301
                if not (O0000O00O0OO0OO0O ):#line:1307
                    if _OOOO0O0000OOOO000 ==1 :#line:1308
                        if len (OOOO00O0O000O0OOO ['cedents_to_do'])==len (OOOO00O0O000O0OOO ['cedents']):#line:1310
                            if O0OO00000000O0O0O .proc =='CFMiner':#line:1311
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verifyCF (_O0OOOO0O0OOO0O0OO )#line:1312
                            elif O0OO00000000O0O0O .proc =='UICMiner':#line:1313
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verifyUIC (_O0OOOO0O0OOO0O0OO )#line:1314
                            elif O0OO00000000O0O0O .proc =='4ftMiner':#line:1315
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verify4ft (_OO000O00O0OO00O00 )#line:1316
                            elif O0OO00000000O0O0O .proc =='SD4ftMiner':#line:1317
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verifysd4ft (_OO000O00O0OO00O00 )#line:1318
                            elif O0OO00000000O0O0O .proc =='NewAct4ftMiner':#line:1319
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verifynewact4ft (_OO000O00O0OO00O00 )#line:1320
                            elif O0OO00000000O0O0O .proc =='Act4ftMiner':#line:1321
                                O000O00000O0OOO00 ,O0O0OO0OOOO0OOO00 =O0OO00000000O0O0O ._verifyact4ft (_OO000O00O0OO00O00 )#line:1322
                            else :#line:1323
                                print ("Unsupported procedure : "+O0OO00000000O0O0O .proc )#line:1324
                                exit (0 )#line:1325
                            if O000O00000O0OOO00 ==True :#line:1326
                                OO0OOO000O0O0O0OO ={}#line:1327
                                OO0OOO000O0O0O0OO ["rule_id"]=O0OO00000000O0O0O .stats ['total_valid']#line:1328
                                OO0OOO000O0O0O0OO ["cedents_str"]={}#line:1329
                                OO0OOO000O0O0O0OO ["cedents_struct"]={}#line:1330
                                OO0OOO000O0O0O0OO ['traces']={}#line:1331
                                OO0OOO000O0O0O0OO ['trace_cedent_taskorder']={}#line:1332
                                OO0OOO000O0O0O0OO ['trace_cedent_dataorder']={}#line:1333
                                for OO0OOO0OOOOOOO000 in OOOO00O0O000O0OOO ['cedents']:#line:1334
                                    OO0OOO000O0O0O0OO ['cedents_str'][OO0OOO0OOOOOOO000 ['cedent_type']]=OO0OOO0OOOOOOO000 ['generated_string']#line:1336
                                    OO0OOO000O0O0O0OO ['cedents_struct'][OO0OOO0OOOOOOO000 ['cedent_type']]=OO0OOO0OOOOOOO000 ['rule']#line:1337
                                    OO0OOO000O0O0O0OO ['traces'][OO0OOO0OOOOOOO000 ['cedent_type']]=OO0OOO0OOOOOOO000 ['traces']#line:1338
                                    OO0OOO000O0O0O0OO ['trace_cedent_taskorder'][OO0OOO0OOOOOOO000 ['cedent_type']]=OO0OOO0OOOOOOO000 ['trace_cedent']#line:1339
                                    OO0OOO000O0O0O0OO ['trace_cedent_dataorder'][OO0OOO0OOOOOOO000 ['cedent_type']]=OO0OOO0OOOOOOO000 ['trace_cedent_asindata']#line:1340
                                OO0OOO000O0O0O0OO ["params"]=O0O0OO0OOOO0OOO00 #line:1342
                                O0OO00000000O0O0O ._print_rule (OO0OOO000O0O0O0OO )#line:1344
                                O0OO00000000O0O0O .rulelist .append (OO0OOO000O0O0O0OO )#line:1350
                            O0OO00000000O0O0O .stats ['total_cnt']+=1 #line:1352
                            O0OO00000000O0O0O .stats ['total_ver']+=1 #line:1353
                    if _OOOO0O0000OOOO000 >=0 :#line:1354
                        if len (OOOO00O0O000O0OOO ['cedents_to_do'])>len (OOOO00O0O000O0OOO ['cedents']):#line:1355
                            O0OO00000000O0O0O ._start_cedent (OOOO00O0O000O0OOO ,_OO0O00OOOOO00O000 +_O00000O0O00O0O00O *_O0O0OO0OO00O0OOO0 ,_OO0O00OOOOO00O000 +(_O00000O0O00O0O00O +0.33 )*_O0O0OO0OO00O0OOO0 )#line:1356
                    OOOO00O0O000O0OOO ['cedents'].pop ()#line:1357
                    if (len (_O0O00O0OOO0O0OO00 )<_OOOO0OO0O00OO000O ):#line:1358
                        O0OO00000000O0O0O ._genvar (OOOO00O0O000O0OOO ,OO0O0O0O00OO0OO0O ,_O0O00O0OOO0O0OO00 ,_O0O0O0000OOO0OOO0 ,_O0OOOO0O0OOO0O0OO ,_O00000O0O0OO00O00 ,_OOOO0OO0O00OO000O ,_OO0O00OOOOO00O000 +(_O00000O0O00O0O00O +0.33 )*_O0O0OO0OO00O0OOO0 ,_OO0O00OOOOO00O000 +(_O00000O0O00O0O00O +0.66 )*_O0O0OO0OO00O0OOO0 )#line:1359
                else :#line:1360
                    OOOO00O0O000O0OOO ['cedents'].pop ()#line:1361
                if len (_OOOOO00O00O000OO0 )<_O0000O0000O0O0OOO :#line:1362
                    O0OO00000000O0O0O ._gencomb (OOOO00O0O000O0OOO ,OO0O0O0O00OO0OO0O ,_O0O00O0OOO0O0OO00 ,_O0O0O0000OOO0OOO0 ,_OOOOO00O00O000OO0 ,_O00OOO0OOOOOOOOO0 ,_OO000O00O0OO00O00 ,OO0O00O0OO0O0OO0O ,_OO0OOO000OOOOOOO0 ,_O00000O0O0OO00O00 ,_OOOO0OO0O00OO000O ,_OO000O0OOO000O0O0 ,_O0000O0000O0O0OOO ,_OO0O00OOOOO00O000 +_O0O0OO0OO00O0OOO0 *(_O00000O0O00O0O00O +0.66 ),_OO0O00OOOOO00O000 +_O0O0OO0OO00O0OOO0 *(_O00000O0O00O0O00O +1 ))#line:1363
                _OOOOO00O00O000OO0 .pop ()#line:1364
                _O00000O0O00O0O00O +=1 #line:1365
                if O0OO00000000O0O0O .options ['progressbar']:#line:1366
                    O0OO00000000O0O0O .bar .update (min (100 ,_OO0O00OOOOO00O000 +_O0O0OO0OO00O0OOO0 *_O00000O0O00O0O00O ))#line:1367
    def _start_cedent (OO0O0000O0O0O0O0O ,O00O000000OO00000 ,_O0000000OOOOO0000 ,_OO0OO0OO0OOOOO0O0 ):#line:1370
        if len (O00O000000OO00000 ['cedents_to_do'])>len (O00O000000OO00000 ['cedents']):#line:1371
            _O0O0OOO0OOO0OO00O =[]#line:1372
            _OOO00OO0000OO0O0O =[]#line:1373
            OOOOO0O0O000O000O ={}#line:1374
            OOOOO0O0O000O000O ['cedent_type']=O00O000000OO00000 ['cedents_to_do'][len (O00O000000OO00000 ['cedents'])]#line:1375
            OOOO00O0OOOOOOOOO =OOOOO0O0O000O000O ['cedent_type']#line:1376
            if ((OOOO00O0OOOOOOOOO [-1 ]=='-')|(OOOO00O0OOOOOOOOO [-1 ]=='+')):#line:1377
                OOOO00O0OOOOOOOOO =OOOO00O0OOOOOOOOO [:-1 ]#line:1378
            OOOOO0O0O000O000O ['defi']=OO0O0000O0O0O0O0O .kwargs .get (OOOO00O0OOOOOOOOO )#line:1380
            if (OOOOO0O0O000O000O ['defi']==None ):#line:1381
                print ("Error getting cedent ",OOOOO0O0O000O000O ['cedent_type'])#line:1382
            _O0OOOO0O0OOO000O0 =int (0 )#line:1383
            OOOOO0O0O000O000O ['num_cedent']=len (OOOOO0O0O000O000O ['defi'].get ('attributes'))#line:1390
            if (OOOOO0O0O000O000O ['defi'].get ('type')=='con'):#line:1391
                _O0OOOO0O0OOO000O0 =(1 <<OO0O0000O0O0O0O0O .data ["rows_count"])-1 #line:1392
            OO0O0000O0O0O0O0O ._genvar (O00O000000OO00000 ,OOOOO0O0O000O000O ,_O0O0OOO0OOO0OO00O ,_OOO00OO0000OO0O0O ,_O0OOOO0O0OOO000O0 ,OOOOO0O0O000O000O ['defi'].get ('minlen'),OOOOO0O0O000O000O ['defi'].get ('maxlen'),_O0000000OOOOO0000 ,_OO0OO0OO0OOOOO0O0 )#line:1393
    def _calc_all (O0O0OO0O0O0OO000O ,**OOOOO00OOOOOO0OOO ):#line:1396
        if "df"in OOOOO00OOOOOO0OOO :#line:1397
            O0O0OO0O0O0OO000O ._prep_data (O0O0OO0O0O0OO000O .kwargs .get ("df"))#line:1398
        if not (O0O0OO0O0O0OO000O ._initialized ):#line:1399
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1400
        else :#line:1401
            O0O0OO0O0O0OO000O ._calculate (**OOOOO00OOOOOO0OOO )#line:1402
    def _check_cedents (OO0O00O000OOO0000 ,O000OO0O000O0OOOO ,**O00000O00O0O0000O ):#line:1404
        OO0O000O0OO0OOOO0 =True #line:1405
        if (O00000O00O0O0000O .get ('quantifiers',None )==None ):#line:1406
            print (f"Error: missing quantifiers.")#line:1407
            OO0O000O0OO0OOOO0 =False #line:1408
            return OO0O000O0OO0OOOO0 #line:1409
        if (type (O00000O00O0O0000O .get ('quantifiers'))!=dict ):#line:1410
            print (f"Error: quantifiers are not dictionary type.")#line:1411
            OO0O000O0OO0OOOO0 =False #line:1412
            return OO0O000O0OO0OOOO0 #line:1413
        for O00O0OO00OOOO0O0O in O000OO0O000O0OOOO :#line:1415
            if (O00000O00O0O0000O .get (O00O0OO00OOOO0O0O ,None )==None ):#line:1416
                print (f"Error: cedent {O00O0OO00OOOO0O0O} is missing in parameters.")#line:1417
                OO0O000O0OO0OOOO0 =False #line:1418
                return OO0O000O0OO0OOOO0 #line:1419
            OOOO0OO00O0O00O00 =O00000O00O0O0000O .get (O00O0OO00OOOO0O0O )#line:1420
            if (OOOO0OO00O0O00O00 .get ('minlen'),None )==None :#line:1421
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has no minimal length specified.")#line:1422
                OO0O000O0OO0OOOO0 =False #line:1423
                return OO0O000O0OO0OOOO0 #line:1424
            if not (type (OOOO0OO00O0O00O00 .get ('minlen'))is int ):#line:1425
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has invalid type of minimal length ({type(OOOO0OO00O0O00O00.get('minlen'))}).")#line:1426
                OO0O000O0OO0OOOO0 =False #line:1427
                return OO0O000O0OO0OOOO0 #line:1428
            if (OOOO0OO00O0O00O00 .get ('maxlen'),None )==None :#line:1429
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has no maximal length specified.")#line:1430
                OO0O000O0OO0OOOO0 =False #line:1431
                return OO0O000O0OO0OOOO0 #line:1432
            if not (type (OOOO0OO00O0O00O00 .get ('maxlen'))is int ):#line:1433
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has invalid type of maximal length.")#line:1434
                OO0O000O0OO0OOOO0 =False #line:1435
                return OO0O000O0OO0OOOO0 #line:1436
            if (OOOO0OO00O0O00O00 .get ('type'),None )==None :#line:1437
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has no type specified.")#line:1438
                OO0O000O0OO0OOOO0 =False #line:1439
                return OO0O000O0OO0OOOO0 #line:1440
            if not ((OOOO0OO00O0O00O00 .get ('type'))in (['con','dis'])):#line:1441
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has invalid type. Allowed values are 'con' and 'dis'.")#line:1442
                OO0O000O0OO0OOOO0 =False #line:1443
                return OO0O000O0OO0OOOO0 #line:1444
            if (OOOO0OO00O0O00O00 .get ('attributes'),None )==None :#line:1445
                print (f"Error: cedent {O00O0OO00OOOO0O0O} has no attributes specified.")#line:1446
                OO0O000O0OO0OOOO0 =False #line:1447
                return OO0O000O0OO0OOOO0 #line:1448
            for OOOOO0OOO00OO000O in OOOO0OO00O0O00O00 .get ('attributes'):#line:1449
                if (OOOOO0OOO00OO000O .get ('name'),None )==None :#line:1450
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O} has no 'name' attribute specified.")#line:1451
                    OO0O000O0OO0OOOO0 =False #line:1452
                    return OO0O000O0OO0OOOO0 #line:1453
                if not ((OOOOO0OOO00OO000O .get ('name'))in OO0O00O000OOO0000 .data ["varname"]):#line:1454
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} not in variable list. Please check spelling.")#line:1455
                    OO0O000O0OO0OOOO0 =False #line:1456
                    return OO0O000O0OO0OOOO0 #line:1457
                if (OOOOO0OOO00OO000O .get ('type'),None )==None :#line:1458
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has no 'type' attribute specified.")#line:1459
                    OO0O000O0OO0OOOO0 =False #line:1460
                    return OO0O000O0OO0OOOO0 #line:1461
                if not ((OOOOO0OOO00OO000O .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1462
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has unsupported type {OOOOO0OOO00OO000O.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1463
                    OO0O000O0OO0OOOO0 =False #line:1464
                    return OO0O000O0OO0OOOO0 #line:1465
                if (OOOOO0OOO00OO000O .get ('minlen'),None )==None :#line:1466
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has no minimal length specified.")#line:1467
                    OO0O000O0OO0OOOO0 =False #line:1468
                    return OO0O000O0OO0OOOO0 #line:1469
                if not (type (OOOOO0OOO00OO000O .get ('minlen'))is int ):#line:1470
                    if not (OOOOO0OOO00OO000O .get ('type')=='one'):#line:1471
                        print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has invalid type of minimal length.")#line:1472
                        OO0O000O0OO0OOOO0 =False #line:1473
                        return OO0O000O0OO0OOOO0 #line:1474
                if (OOOOO0OOO00OO000O .get ('maxlen'),None )==None :#line:1475
                    print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has no maximal length specified.")#line:1476
                    OO0O000O0OO0OOOO0 =False #line:1477
                    return OO0O000O0OO0OOOO0 #line:1478
                if not (type (OOOOO0OOO00OO000O .get ('maxlen'))is int ):#line:1479
                    if not (OOOOO0OOO00OO000O .get ('type')=='one'):#line:1480
                        print (f"Error: cedent {O00O0OO00OOOO0O0O} / attribute {OOOOO0OOO00OO000O.get('name')} has invalid type of maximal length.")#line:1481
                        OO0O000O0OO0OOOO0 =False #line:1482
                        return OO0O000O0OO0OOOO0 #line:1483
        return OO0O000O0OO0OOOO0 #line:1484
    def _calculate (O0OO00OO00000OOOO ,**OO0O0000OO0O000OO ):#line:1486
        if O0OO00OO00000OOOO .data ["data_prepared"]==0 :#line:1487
            print ("Error: data not prepared")#line:1488
            return #line:1489
        O0OO00OO00000OOOO .kwargs =OO0O0000OO0O000OO #line:1490
        O0OO00OO00000OOOO .proc =OO0O0000OO0O000OO .get ('proc')#line:1491
        O0OO00OO00000OOOO .quantifiers =OO0O0000OO0O000OO .get ('quantifiers')#line:1492
        O0OO00OO00000OOOO ._init_task ()#line:1494
        O0OO00OO00000OOOO .stats ['start_proc_time']=time .time ()#line:1495
        O0OO00OO00000OOOO .task_actinfo ['cedents_to_do']=[]#line:1496
        O0OO00OO00000OOOO .task_actinfo ['cedents']=[]#line:1497
        if OO0O0000OO0O000OO .get ("proc")=='UICMiner':#line:1500
            if not (O0OO00OO00000OOOO ._check_cedents (['ante'],**OO0O0000OO0O000OO )):#line:1501
                return #line:1502
            _OOO0O0O00OOO0000O =OO0O0000OO0O000OO .get ("cond")#line:1504
            if _OOO0O0O00OOO0000O !=None :#line:1505
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1506
            else :#line:1507
                OOO00O00OOOOOO000 =O0OO00OO00000OOOO .cedent #line:1508
                OOO00O00OOOOOO000 ['cedent_type']='cond'#line:1509
                OOO00O00OOOOOO000 ['filter_value']=(1 <<O0OO00OO00000OOOO .data ["rows_count"])-1 #line:1510
                OOO00O00OOOOOO000 ['generated_string']='---'#line:1511
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1513
                O0OO00OO00000OOOO .task_actinfo ['cedents'].append (OOO00O00OOOOOO000 )#line:1514
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1515
            if OO0O0000OO0O000OO .get ('target',None )==None :#line:1516
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1517
                return #line:1518
            if not (OO0O0000OO0O000OO .get ('target')in O0OO00OO00000OOOO .data ["varname"]):#line:1519
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1520
                return #line:1521
            if ("aad_score"in O0OO00OO00000OOOO .quantifiers ):#line:1522
                if not ("aad_weights"in O0OO00OO00000OOOO .quantifiers ):#line:1523
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1524
                    return #line:1525
                if not (len (O0OO00OO00000OOOO .quantifiers .get ("aad_weights"))==len (O0OO00OO00000OOOO .data ["dm"][O0OO00OO00000OOOO .data ["varname"].index (O0OO00OO00000OOOO .kwargs .get ('target'))])):#line:1526
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1527
                    return #line:1528
        elif OO0O0000OO0O000OO .get ("proc")=='CFMiner':#line:1529
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do']=['cond']#line:1530
            if OO0O0000OO0O000OO .get ('target',None )==None :#line:1531
                print ("ERROR: no target variable defined for CF Miner")#line:1532
                return #line:1533
            if not (O0OO00OO00000OOOO ._check_cedents (['cond'],**OO0O0000OO0O000OO )):#line:1534
                return #line:1535
            if not (OO0O0000OO0O000OO .get ('target')in O0OO00OO00000OOOO .data ["varname"]):#line:1536
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1537
                return #line:1538
            if ("aad"in O0OO00OO00000OOOO .quantifiers ):#line:1539
                if not ("aad_weights"in O0OO00OO00000OOOO .quantifiers ):#line:1540
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1541
                    return #line:1542
                if not (len (O0OO00OO00000OOOO .quantifiers .get ("aad_weights"))==len (O0OO00OO00000OOOO .data ["dm"][O0OO00OO00000OOOO .data ["varname"].index (O0OO00OO00000OOOO .kwargs .get ('target'))])):#line:1543
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1544
                    return #line:1545
        elif OO0O0000OO0O000OO .get ("proc")=='4ftMiner':#line:1548
            if not (O0OO00OO00000OOOO ._check_cedents (['ante','succ'],**OO0O0000OO0O000OO )):#line:1549
                return #line:1550
            _OOO0O0O00OOO0000O =OO0O0000OO0O000OO .get ("cond")#line:1552
            if _OOO0O0O00OOO0000O !=None :#line:1553
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1554
            else :#line:1555
                OOO00O00OOOOOO000 =O0OO00OO00000OOOO .cedent #line:1556
                OOO00O00OOOOOO000 ['cedent_type']='cond'#line:1557
                OOO00O00OOOOOO000 ['filter_value']=(1 <<O0OO00OO00000OOOO .data ["rows_count"])-1 #line:1558
                OOO00O00OOOOOO000 ['generated_string']='---'#line:1559
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1561
                O0OO00OO00000OOOO .task_actinfo ['cedents'].append (OOO00O00OOOOOO000 )#line:1562
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1566
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1567
        elif OO0O0000OO0O000OO .get ("proc")=='NewAct4ftMiner':#line:1568
            _OOO0O0O00OOO0000O =OO0O0000OO0O000OO .get ("cond")#line:1571
            if _OOO0O0O00OOO0000O !=None :#line:1572
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1573
            else :#line:1574
                OOO00O00OOOOOO000 =O0OO00OO00000OOOO .cedent #line:1575
                OOO00O00OOOOOO000 ['cedent_type']='cond'#line:1576
                OOO00O00OOOOOO000 ['filter_value']=(1 <<O0OO00OO00000OOOO .data ["rows_count"])-1 #line:1577
                OOO00O00OOOOOO000 ['generated_string']='---'#line:1578
                print (OOO00O00OOOOOO000 ['filter_value'])#line:1579
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1580
                O0OO00OO00000OOOO .task_actinfo ['cedents'].append (OOO00O00OOOOOO000 )#line:1581
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('antv')#line:1582
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('sucv')#line:1583
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1584
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1585
        elif OO0O0000OO0O000OO .get ("proc")=='Act4ftMiner':#line:1586
            _OOO0O0O00OOO0000O =OO0O0000OO0O000OO .get ("cond")#line:1589
            if _OOO0O0O00OOO0000O !=None :#line:1590
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1591
            else :#line:1592
                OOO00O00OOOOOO000 =O0OO00OO00000OOOO .cedent #line:1593
                OOO00O00OOOOOO000 ['cedent_type']='cond'#line:1594
                OOO00O00OOOOOO000 ['filter_value']=(1 <<O0OO00OO00000OOOO .data ["rows_count"])-1 #line:1595
                OOO00O00OOOOOO000 ['generated_string']='---'#line:1596
                print (OOO00O00OOOOOO000 ['filter_value'])#line:1597
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1598
                O0OO00OO00000OOOO .task_actinfo ['cedents'].append (OOO00O00OOOOOO000 )#line:1599
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('antv-')#line:1600
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('antv+')#line:1601
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1602
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1603
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1604
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1605
        elif OO0O0000OO0O000OO .get ("proc")=='SD4ftMiner':#line:1606
            if not (O0OO00OO00000OOOO ._check_cedents (['ante','succ','frst','scnd'],**OO0O0000OO0O000OO )):#line:1609
                return #line:1610
            _OOO0O0O00OOO0000O =OO0O0000OO0O000OO .get ("cond")#line:1611
            if _OOO0O0O00OOO0000O !=None :#line:1612
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1613
            else :#line:1614
                OOO00O00OOOOOO000 =O0OO00OO00000OOOO .cedent #line:1615
                OOO00O00OOOOOO000 ['cedent_type']='cond'#line:1616
                OOO00O00OOOOOO000 ['filter_value']=(1 <<O0OO00OO00000OOOO .data ["rows_count"])-1 #line:1617
                OOO00O00OOOOOO000 ['generated_string']='---'#line:1618
                O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('cond')#line:1620
                O0OO00OO00000OOOO .task_actinfo ['cedents'].append (OOO00O00OOOOOO000 )#line:1621
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('frst')#line:1622
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('scnd')#line:1623
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('ante')#line:1624
            O0OO00OO00000OOOO .task_actinfo ['cedents_to_do'].append ('succ')#line:1625
        else :#line:1626
            print ("Unsupported procedure")#line:1627
            return #line:1628
        print ("Will go for ",OO0O0000OO0O000OO .get ("proc"))#line:1629
        O0OO00OO00000OOOO .task_actinfo ['optim']={}#line:1632
        OOOO00OO0OO00000O =True #line:1633
        for OOOOO0O0O00O0000O in O0OO00OO00000OOOO .task_actinfo ['cedents_to_do']:#line:1634
            try :#line:1635
                OO00OO0OO000OOO00 =O0OO00OO00000OOOO .kwargs .get (OOOOO0O0O00O0000O )#line:1636
                if OO00OO0OO000OOO00 .get ('type')!='con':#line:1640
                    OOOO00OO0OO00000O =False #line:1641
            except :#line:1643
                OO0000000O0OOO000 =1 <2 #line:1644
        if O0OO00OO00000OOOO .options ['optimizations']==False :#line:1646
            OOOO00OO0OO00000O =False #line:1647
        OOO00OOO00O00OO00 ={}#line:1648
        OOO00OOO00O00OO00 ['only_con']=OOOO00OO0OO00000O #line:1649
        O0OO00OO00000OOOO .task_actinfo ['optim']=OOO00OOO00O00OO00 #line:1650
        print ("Starting to mine rules.")#line:1658
        sys .stdout .flush ()#line:1659
        time .sleep (0.01 )#line:1660
        if O0OO00OO00000OOOO .options ['progressbar']:#line:1661
            OO000OOO0OOO0O00O =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:1662
            O0OO00OO00000OOOO .bar =progressbar .ProgressBar (widgets =OO000OOO0OOO0O00O ,max_value =100 ,fd =sys .stdout ).start ()#line:1663
            O0OO00OO00000OOOO .bar .update (0 )#line:1664
        O0OO00OO00000OOOO .progress_lower =0 #line:1665
        O0OO00OO00000OOOO .progress_upper =100 #line:1666
        O0OO00OO00000OOOO ._start_cedent (O0OO00OO00000OOOO .task_actinfo ,O0OO00OO00000OOOO .progress_lower ,O0OO00OO00000OOOO .progress_upper )#line:1667
        if O0OO00OO00000OOOO .options ['progressbar']:#line:1668
            O0OO00OO00000OOOO .bar .update (100 )#line:1669
            O0OO00OO00000OOOO .bar .finish ()#line:1670
        O0OO00OO00000OOOO .stats ['end_proc_time']=time .time ()#line:1672
        print ("Done. Total verifications : "+str (O0OO00OO00000OOOO .stats ['total_cnt'])+", rules "+str (O0OO00OO00000OOOO .stats ['total_valid'])+", times: prep "+"{:.2f}".format (O0OO00OO00000OOOO .stats ['end_prep_time']-O0OO00OO00000OOOO .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (O0OO00OO00000OOOO .stats ['end_proc_time']-O0OO00OO00000OOOO .stats ['start_proc_time'])+"sec")#line:1676
        OO0OO0O0000OO0OO0 ={}#line:1677
        OO0OOO0O0O0OOO000 ={}#line:1678
        OO0OOO0O0O0OOO000 ["task_type"]=OO0O0000OO0O000OO .get ('proc')#line:1679
        OO0OOO0O0O0OOO000 ["target"]=OO0O0000OO0O000OO .get ('target')#line:1681
        OO0OOO0O0O0OOO000 ["self.quantifiers"]=O0OO00OO00000OOOO .quantifiers #line:1682
        if OO0O0000OO0O000OO .get ('cond')!=None :#line:1684
            OO0OOO0O0O0OOO000 ['cond']=OO0O0000OO0O000OO .get ('cond')#line:1685
        if OO0O0000OO0O000OO .get ('ante')!=None :#line:1686
            OO0OOO0O0O0OOO000 ['ante']=OO0O0000OO0O000OO .get ('ante')#line:1687
        if OO0O0000OO0O000OO .get ('succ')!=None :#line:1688
            OO0OOO0O0O0OOO000 ['succ']=OO0O0000OO0O000OO .get ('succ')#line:1689
        if OO0O0000OO0O000OO .get ('opts')!=None :#line:1690
            OO0OOO0O0O0OOO000 ['opts']=OO0O0000OO0O000OO .get ('opts')#line:1691
        if O0OO00OO00000OOOO .df is None :#line:1692
            OO0OOO0O0O0OOO000 ['rowcount']=len (OO0O0000OO0O000OO .get ('df').index )#line:1693
        else :#line:1694
            OO0OOO0O0O0OOO000 ['rowcount']=len (O0OO00OO00000OOOO .df .index )#line:1695
        OO0OO0O0000OO0OO0 ["taskinfo"]=OO0OOO0O0O0OOO000 #line:1696
        O00OO0O000O0O0OO0 ={}#line:1697
        O00OO0O000O0O0OO0 ["total_verifications"]=O0OO00OO00000OOOO .stats ['total_cnt']#line:1698
        O00OO0O000O0O0OO0 ["valid_rules"]=O0OO00OO00000OOOO .stats ['total_valid']#line:1699
        O00OO0O000O0O0OO0 ["total_verifications_with_opt"]=O0OO00OO00000OOOO .stats ['total_ver']#line:1700
        O00OO0O000O0O0OO0 ["time_prep"]=O0OO00OO00000OOOO .stats ['end_prep_time']-O0OO00OO00000OOOO .stats ['start_prep_time']#line:1701
        O00OO0O000O0O0OO0 ["time_processing"]=O0OO00OO00000OOOO .stats ['end_proc_time']-O0OO00OO00000OOOO .stats ['start_proc_time']#line:1702
        O00OO0O000O0O0OO0 ["time_total"]=O0OO00OO00000OOOO .stats ['end_prep_time']-O0OO00OO00000OOOO .stats ['start_prep_time']+O0OO00OO00000OOOO .stats ['end_proc_time']-O0OO00OO00000OOOO .stats ['start_proc_time']#line:1703
        OO0OO0O0000OO0OO0 ["summary_statistics"]=O00OO0O000O0O0OO0 #line:1704
        OO0OO0O0000OO0OO0 ["rules"]=O0OO00OO00000OOOO .rulelist #line:1705
        O00OO00OOOO0OO0O0 ={}#line:1706
        O00OO00OOOO0OO0O0 ["varname"]=O0OO00OO00000OOOO .data ["varname"]#line:1707
        O00OO00OOOO0OO0O0 ["catnames"]=O0OO00OO00000OOOO .data ["catnames"]#line:1708
        OO0OO0O0000OO0OO0 ["datalabels"]=O00OO00OOOO0OO0O0 #line:1709
        O0OO00OO00000OOOO .result =OO0OO0O0000OO0OO0 #line:1710
    def print_summary (O0OO000O0OO0O000O ):#line:1712
        ""#line:1715
        if not (O0OO000O0OO0O000O ._is_calculated ()):#line:1716
            print ("ERROR: Task has not been calculated.")#line:1717
            return #line:1718
        print ("")#line:1719
        print ("CleverMiner task processing summary:")#line:1720
        print ("")#line:1721
        print (f"Task type : {O0OO000O0OO0O000O.result['taskinfo']['task_type']}")#line:1722
        print (f"Number of verifications : {O0OO000O0OO0O000O.result['summary_statistics']['total_verifications']}")#line:1723
        print (f"Number of rules : {O0OO000O0OO0O000O.result['summary_statistics']['valid_rules']}")#line:1724
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O0OO000O0OO0O000O.result['summary_statistics']['time_total']))}")#line:1725
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O0OO000O0OO0O000O.result['summary_statistics']['time_prep']))}")#line:1727
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O0OO000O0OO0O000O.result['summary_statistics']['time_processing']))}")#line:1728
        print ("")#line:1729
    def print_hypolist (OOOOOO0000OOOO000 ):#line:1731
        OOOOOO0000OOOO000 .print_rulelist ();#line:1732
    def print_rulelist (O0OOOOOO0O000OO00 ,sortby =None ,storesorted =False ):#line:1734
        if not (O0OOOOOO0O000OO00 ._is_calculated ()):#line:1735
            print ("ERROR: Task has not been calculated.")#line:1736
            return #line:1737
        def OO0OOO0OO0O000OOO (OOOO0OO0OOO00000O ):#line:1738
            O000OOOO0OO0O000O =OOOO0OO0OOO00000O ["params"]#line:1739
            return O000OOOO0OO0O000O .get (sortby ,0 )#line:1740
        print ("")#line:1742
        print ("List of rules:")#line:1743
        if O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1744
            print ("RULEID BASE  CONF  AAD    Rule")#line:1745
        elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1746
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1747
        elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1748
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1749
        elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1750
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1751
        else :#line:1752
            print ("Unsupported task type for rulelist")#line:1753
            return #line:1754
        O00000O000OOO00OO =O0OOOOOO0O000OO00 .result ["rules"]#line:1755
        if sortby is not None :#line:1756
            O00000O000OOO00OO =sorted (O00000O000OOO00OO ,key =OO0OOO0OO0O000OOO ,reverse =True )#line:1757
            if storesorted :#line:1758
                O0OOOOOO0O000OO00 .result ["rules"]=O00000O000OOO00OO #line:1759
        for OO00OOOOOO0000OO0 in O00000O000OOO00OO :#line:1761
            O00O00000000OOOOO ="{:6d}".format (OO00OOOOOO0000OO0 ["rule_id"])#line:1762
            if O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1763
                O00O00000000OOOOO =O00O00000000OOOOO +" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["base"])+" "+"{:.3f}".format (OO00OOOOOO0000OO0 ["params"]["conf"])+" "+"{:+.3f}".format (OO00OOOOOO0000OO0 ["params"]["aad"])#line:1765
                O00O00000000OOOOO =O00O00000000OOOOO +" "+OO00OOOOOO0000OO0 ["cedents_str"]["ante"]+" => "+OO00OOOOOO0000OO0 ["cedents_str"]["succ"]+" | "+OO00OOOOOO0000OO0 ["cedents_str"]["cond"]#line:1766
            elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1767
                O00O00000000OOOOO =O00O00000000OOOOO +" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["base"])+" "+"{:.3f}".format (OO00OOOOOO0000OO0 ["params"]["aad_score"])#line:1768
                O00O00000000OOOOO =O00O00000000OOOOO +"     "+OO00OOOOOO0000OO0 ["cedents_str"]["ante"]+" => "+O0OOOOOO0O000OO00 .result ['taskinfo']['target']+"(*) | "+OO00OOOOOO0000OO0 ["cedents_str"]["cond"]#line:1769
            elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1770
                O00O00000000OOOOO =O00O00000000OOOOO +" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["base"])+" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["s_up"])+" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["s_down"])#line:1771
                O00O00000000OOOOO =O00O00000000OOOOO +" "+OO00OOOOOO0000OO0 ["cedents_str"]["cond"]#line:1772
            elif O0OOOOOO0O000OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1773
                O00O00000000OOOOO =O00O00000000OOOOO +" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["base1"])+" "+"{:5d}".format (OO00OOOOOO0000OO0 ["params"]["base2"])+"    "+"{:.3f}".format (OO00OOOOOO0000OO0 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OO00OOOOOO0000OO0 ["params"]["deltaconf"])#line:1774
                O00O00000000OOOOO =O00O00000000OOOOO +"  "+OO00OOOOOO0000OO0 ["cedents_str"]["ante"]+" => "+OO00OOOOOO0000OO0 ["cedents_str"]["succ"]+" | "+OO00OOOOOO0000OO0 ["cedents_str"]["cond"]+" : "+OO00OOOOOO0000OO0 ["cedents_str"]["frst"]+" x "+OO00OOOOOO0000OO0 ["cedents_str"]["scnd"]#line:1775
            print (O00O00000000OOOOO )#line:1777
        print ("")#line:1778
    def print_hypo (O00OOO0O0OO0O0O00 ,O0O00O0OOOO00000O ):#line:1780
        O00OOO0O0OO0O0O00 .print_rule (O0O00O0OOOO00000O )#line:1781
    def print_rule (O00O00000OO0O0O0O ,O0OOOO0OO0O00OOO0 ):#line:1784
        if not (O00O00000OO0O0O0O ._is_calculated ()):#line:1785
            print ("ERROR: Task has not been calculated.")#line:1786
            return #line:1787
        print ("")#line:1788
        if (O0OOOO0OO0O00OOO0 <=len (O00O00000OO0O0O0O .result ["rules"])):#line:1789
            if O00O00000OO0O0O0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1790
                print ("")#line:1791
                O0OO0000OO00O0OO0 =O00O00000OO0O0O0O .result ["rules"][O0OOOO0OO0O00OOO0 -1 ]#line:1792
                print (f"Rule id : {O0OO0000OO00O0OO0['rule_id']}")#line:1793
                print ("")#line:1794
                print (f"Base : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['base'])}  Relative base : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_base'])}  CONF : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['conf'])}  AAD : {'{:+.3f}'.format(O0OO0000OO00O0OO0['params']['aad'])}  BAD : {'{:+.3f}'.format(O0OO0000OO00O0OO0['params']['bad'])}")#line:1795
                print ("")#line:1796
                print ("Cedents:")#line:1797
                print (f"  antecedent : {O0OO0000OO00O0OO0['cedents_str']['ante']}")#line:1798
                print (f"  succcedent : {O0OO0000OO00O0OO0['cedents_str']['succ']}")#line:1799
                print (f"  condition  : {O0OO0000OO00O0OO0['cedents_str']['cond']}")#line:1800
                print ("")#line:1801
                print ("Fourfold table")#line:1802
                print (f"    |  S  |  ¬S |")#line:1803
                print (f"----|-----|-----|")#line:1804
                print (f" A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold'][0])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold'][1])}|")#line:1805
                print (f"----|-----|-----|")#line:1806
                print (f"¬A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold'][2])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold'][3])}|")#line:1807
                print (f"----|-----|-----|")#line:1808
            elif O00O00000OO0O0O0O .result ['taskinfo']['task_type']=="CFMiner":#line:1809
                print ("")#line:1810
                O0OO0000OO00O0OO0 =O00O00000OO0O0O0O .result ["rules"][O0OOOO0OO0O00OOO0 -1 ]#line:1811
                print (f"Rule id : {O0OO0000OO00O0OO0['rule_id']}")#line:1812
                print ("")#line:1813
                O0O0O000OO0O000O0 =""#line:1814
                if ('aad'in O0OO0000OO00O0OO0 ['params']):#line:1815
                    O0O0O000OO0O000O0 ="aad : "+str (O0OO0000OO00O0OO0 ['params']['aad'])#line:1816
                print (f"Base : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['base'])}  Relative base : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['max'])}  Histogram minimum : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_min'])} {O0O0O000OO0O000O0}")#line:1818
                print ("")#line:1819
                print (f"Condition  : {O0OO0000OO00O0OO0['cedents_str']['cond']}")#line:1820
                print ("")#line:1821
                OO00O0OOOO0O0OO0O =O00O00000OO0O0O0O .get_category_names (O00O00000OO0O0O0O .result ["taskinfo"]["target"])#line:1822
                print (f"Categories in target variable  {OO00O0OOOO0O0OO0O}")#line:1823
                print (f"Histogram                      {O0OO0000OO00O0OO0['params']['hist']}")#line:1824
                if ('aad'in O0OO0000OO00O0OO0 ['params']):#line:1825
                    print (f"Histogram on full set          {O0OO0000OO00O0OO0['params']['hist_full']}")#line:1826
                    print (f"Relative histogram             {O0OO0000OO00O0OO0['params']['rel_hist']}")#line:1827
                    print (f"Relative histogram on full set {O0OO0000OO00O0OO0['params']['rel_hist_full']}")#line:1828
            elif O00O00000OO0O0O0O .result ['taskinfo']['task_type']=="UICMiner":#line:1829
                print ("")#line:1830
                O0OO0000OO00O0OO0 =O00O00000OO0O0O0O .result ["rules"][O0OOOO0OO0O00OOO0 -1 ]#line:1831
                print (f"Rule id : {O0OO0000OO00O0OO0['rule_id']}")#line:1832
                print ("")#line:1833
                O0O0O000OO0O000O0 =""#line:1834
                if ('aad_score'in O0OO0000OO00O0OO0 ['params']):#line:1835
                    O0O0O000OO0O000O0 ="aad score : "+str (O0OO0000OO00O0OO0 ['params']['aad_score'])#line:1836
                print (f"Base : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['base'])}  Relative base : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_base'])}   {O0O0O000OO0O000O0}")#line:1838
                print ("")#line:1839
                print (f"Condition  : {O0OO0000OO00O0OO0['cedents_str']['cond']}")#line:1840
                print (f"Antecedent : {O0OO0000OO00O0OO0['cedents_str']['ante']}")#line:1841
                print ("")#line:1842
                print (f"Histogram                                        {O0OO0000OO00O0OO0['params']['hist']}")#line:1843
                if ('aad_score'in O0OO0000OO00O0OO0 ['params']):#line:1844
                    print (f"Histogram on full set with condition             {O0OO0000OO00O0OO0['params']['hist_cond']}")#line:1845
                    print (f"Relative histogram                               {O0OO0000OO00O0OO0['params']['rel_hist']}")#line:1846
                    print (f"Relative histogram on full set with condition    {O0OO0000OO00O0OO0['params']['rel_hist_cond']}")#line:1847
                OO00OOOOO0OO0000O =O00O00000OO0O0O0O .result ['datalabels']['catnames'][O00O00000OO0O0O0O .result ['datalabels']['varname'].index (O00O00000OO0O0O0O .result ['taskinfo']['target'])]#line:1848
                print (" ")#line:1850
                print ("Interpretation:")#line:1851
                for OO00O000OO0OO0O00 in range (len (OO00OOOOO0OO0000O )):#line:1852
                  OO0O0O000000OO000 =0 #line:1853
                  if O0OO0000OO00O0OO0 ['params']['rel_hist'][OO00O000OO0OO0O00 ]>0 :#line:1854
                      OO0O0O000000OO000 =O0OO0000OO00O0OO0 ['params']['rel_hist'][OO00O000OO0OO0O00 ]/O0OO0000OO00O0OO0 ['params']['rel_hist_cond'][OO00O000OO0OO0O00 ]#line:1855
                  O00O0O0000O000000 =''#line:1856
                  if not (O0OO0000OO00O0OO0 ['cedents_str']['cond']=='---'):#line:1857
                      O00O0O0000O000000 ="For "+O0OO0000OO00O0OO0 ['cedents_str']['cond']+": "#line:1858
                  print (f"    {O00O0O0000O000000}{O00O00000OO0O0O0O.result['taskinfo']['target']}({OO00OOOOO0OO0000O[OO00O000OO0OO0O00]}) has occurence {'{:.1%}'.format(O0OO0000OO00O0OO0['params']['rel_hist_cond'][OO00O000OO0OO0O00])}, with antecedent it has occurence {'{:.1%}'.format(O0OO0000OO00O0OO0['params']['rel_hist'][OO00O000OO0OO0O00])}, that is {'{:.3f}'.format(OO0O0O000000OO000)} times more.")#line:1860
            elif O00O00000OO0O0O0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1861
                print ("")#line:1862
                O0OO0000OO00O0OO0 =O00O00000OO0O0O0O .result ["rules"][O0OOOO0OO0O00OOO0 -1 ]#line:1863
                print (f"Rule id : {O0OO0000OO00O0OO0['rule_id']}")#line:1864
                print ("")#line:1865
                print (f"Base1 : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['base1'])} Base2 : {'{:5d}'.format(O0OO0000OO00O0OO0['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O0OO0000OO00O0OO0['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O0OO0000OO00O0OO0['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O0OO0000OO00O0OO0['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O0OO0000OO00O0OO0['params']['ratioconf'])}")#line:1866
                print ("")#line:1867
                print ("Cedents:")#line:1868
                print (f"  antecedent : {O0OO0000OO00O0OO0['cedents_str']['ante']}")#line:1869
                print (f"  succcedent : {O0OO0000OO00O0OO0['cedents_str']['succ']}")#line:1870
                print (f"  condition  : {O0OO0000OO00O0OO0['cedents_str']['cond']}")#line:1871
                print (f"  first set  : {O0OO0000OO00O0OO0['cedents_str']['frst']}")#line:1872
                print (f"  second set : {O0OO0000OO00O0OO0['cedents_str']['scnd']}")#line:1873
                print ("")#line:1874
                print ("Fourfold tables:")#line:1875
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1876
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1877
                print (f" A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold1'][0])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold2'][0])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold2'][1])}|")#line:1878
                print (f"----|-----|-----|  ----|-----|-----|")#line:1879
                print (f"¬A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold1'][2])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold2'][2])}|{'{:5d}'.format(O0OO0000OO00O0OO0['params']['fourfold2'][3])}|")#line:1880
                print (f"----|-----|-----|  ----|-----|-----|")#line:1881
            else :#line:1882
                print ("Unsupported task type for rule details")#line:1883
            print ("")#line:1887
        else :#line:1888
            print ("No such rule.")#line:1889
    def get_rulecount (OOO0OOO00OOOO000O ):#line:1891
        if not (OOO0OOO00OOOO000O ._is_calculated ()):#line:1892
            print ("ERROR: Task has not been calculated.")#line:1893
            return #line:1894
        return len (OOO0OOO00OOOO000O .result ["rules"])#line:1895
    def get_ruletext (O0000O0000O0OOO0O ,OOOO0OOOO0OO0OO00 ):#line:1897
        ""#line:1903
        if not (O0000O0000O0OOO0O ._is_calculated ()):#line:1904
            print ("ERROR: Task has not been calculated.")#line:1905
            return #line:1906
        if OOOO0OOOO0OO0OO00 <=0 or OOOO0OOOO0OO0OO00 >O0000O0000O0OOO0O .get_rulecount ():#line:1907
            if O0000O0000O0OOO0O .get_rulecount ()==0 :#line:1908
                print ("No such rule. There are no rules in result.")#line:1909
            else :#line:1910
                print (f"No such rule ({OOOO0OOOO0OO0OO00}). Available rules are 1 to {O0000O0000O0OOO0O.get_rulecount()}")#line:1911
            return None #line:1912
        OOO0O0000O0O0OO00 =""#line:1913
        O00O0O0OO000O0000 =O0000O0000O0OOO0O .result ["rules"][OOOO0OOOO0OO0OO00 -1 ]#line:1914
        if O0000O0000O0OOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1915
            OOO0O0000O0O0OO00 =OOO0O0000O0O0OO00 +" "+O00O0O0OO000O0000 ["cedents_str"]["ante"]+" => "+O00O0O0OO000O0000 ["cedents_str"]["succ"]+" | "+O00O0O0OO000O0000 ["cedents_str"]["cond"]#line:1917
        elif O0000O0000O0OOO0O .result ['taskinfo']['task_type']=="UICMiner":#line:1918
            OOO0O0000O0O0OO00 =OOO0O0000O0O0OO00 +"     "+O00O0O0OO000O0000 ["cedents_str"]["ante"]+" => "+O0000O0000O0OOO0O .result ['taskinfo']['target']+"(*) | "+O00O0O0OO000O0000 ["cedents_str"]["cond"]#line:1920
        elif O0000O0000O0OOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1921
            OOO0O0000O0O0OO00 =OOO0O0000O0O0OO00 +" "+O00O0O0OO000O0000 ["cedents_str"]["cond"]#line:1922
        elif O0000O0000O0OOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1923
            OOO0O0000O0O0OO00 =OOO0O0000O0O0OO00 +"  "+O00O0O0OO000O0000 ["cedents_str"]["ante"]+" => "+O00O0O0OO000O0000 ["cedents_str"]["succ"]+" | "+O00O0O0OO000O0000 ["cedents_str"]["cond"]+" : "+O00O0O0OO000O0000 ["cedents_str"]["frst"]+" x "+O00O0O0OO000O0000 ["cedents_str"]["scnd"]#line:1925
        return OOO0O0000O0O0OO00 #line:1926
    def get_fourfold (O0O00OOOO000O0OOO ,OOO0OO0O00000000O ,order =0 ):#line:1928
        if not (O0O00OOOO000O0OOO ._is_calculated ()):#line:1929
            print ("ERROR: Task has not been calculated.")#line:1930
            return #line:1931
        if (OOO0OO0O00000000O <=len (O0O00OOOO000O0OOO .result ["rules"])):#line:1932
            if O0O00OOOO000O0OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1933
                OO0OO00O00O0OO0OO =O0O00OOOO000O0OOO .result ["rules"][OOO0OO0O00000000O -1 ]#line:1934
                return OO0OO00O00O0OO0OO ['params']['fourfold']#line:1935
            elif O0O00OOOO000O0OOO .result ['taskinfo']['task_type']=="CFMiner":#line:1936
                print ("Error: fourfold for CFMiner is not defined")#line:1937
                return None #line:1938
            elif O0O00OOOO000O0OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1939
                OO0OO00O00O0OO0OO =O0O00OOOO000O0OOO .result ["rules"][OOO0OO0O00000000O -1 ]#line:1940
                if order ==1 :#line:1941
                    return OO0OO00O00O0OO0OO ['params']['fourfold1']#line:1942
                if order ==2 :#line:1943
                    return OO0OO00O00O0OO0OO ['params']['fourfold2']#line:1944
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1945
                return None #line:1946
            else :#line:1947
                print ("Unsupported task type for rule details")#line:1948
        else :#line:1949
            print ("No such rule.")#line:1950
    def get_hist (O00O000OOOOOO00OO ,O0O0O0000O00OOOO0 ):#line:1952
        if not (O00O000OOOOOO00OO ._is_calculated ()):#line:1953
            print ("ERROR: Task has not been calculated.")#line:1954
            return #line:1955
        if (O0O0O0000O00OOOO0 <=len (O00O000OOOOOO00OO .result ["rules"])):#line:1956
            if O00O000OOOOOO00OO .result ['taskinfo']['task_type']=="CFMiner":#line:1957
                O00000OOOO0O000OO =O00O000OOOOOO00OO .result ["rules"][O0O0O0000O00OOOO0 -1 ]#line:1958
                return O00000OOOO0O000OO ['params']['hist']#line:1959
            elif O00O000OOOOOO00OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1960
                print ("Error: SD4ft-Miner has no histogram")#line:1961
                return None #line:1962
            elif O00O000OOOOOO00OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1963
                print ("Error: 4ft-Miner has no histogram")#line:1964
                return None #line:1965
            else :#line:1966
                print ("Unsupported task type for rule details")#line:1967
        else :#line:1968
            print ("No such rule.")#line:1969
    def get_hist_cond (OO0O00000OO0O0O00 ,OO0000OOOOO0OOO00 ):#line:1972
        if not (OO0O00000OO0O0O00 ._is_calculated ()):#line:1973
            print ("ERROR: Task has not been calculated.")#line:1974
            return #line:1975
        if (OO0000OOOOO0OOO00 <=len (OO0O00000OO0O0O00 .result ["rules"])):#line:1976
            if OO0O00000OO0O0O00 .result ['taskinfo']['task_type']=="UICMiner":#line:1977
                O0OOOO00O0OOOO00O =OO0O00000OO0O0O00 .result ["rules"][OO0000OOOOO0OOO00 -1 ]#line:1978
                return O0OOOO00O0OOOO00O ['params']['hist_cond']#line:1979
            elif OO0O00000OO0O0O00 .result ['taskinfo']['task_type']=="CFMiner":#line:1980
                O0OOOO00O0OOOO00O =OO0O00000OO0O0O00 .result ["rules"][OO0000OOOOO0OOO00 -1 ]#line:1981
                return O0OOOO00O0OOOO00O ['params']['hist']#line:1982
            elif OO0O00000OO0O0O00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1983
                print ("Error: SD4ft-Miner has no histogram")#line:1984
                return None #line:1985
            elif OO0O00000OO0O0O00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1986
                print ("Error: 4ft-Miner has no histogram")#line:1987
                return None #line:1988
            else :#line:1989
                print ("Unsupported task type for rule details")#line:1990
        else :#line:1991
            print ("No such rule.")#line:1992
    def get_quantifiers (O0OO0O00000O0OO00 ,OOOO00O000000O00O ,order =0 ):#line:1994
        if not (O0OO0O00000O0OO00 ._is_calculated ()):#line:1995
            print ("ERROR: Task has not been calculated.")#line:1996
            return #line:1997
        if (OOOO00O000000O00O <=len (O0OO0O00000O0OO00 .result ["rules"])):#line:1998
            O00OOOO00OO0OO0O0 =O0OO0O00000O0OO00 .result ["rules"][OOOO00O000000O00O -1 ]#line:1999
            if O0OO0O00000O0OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:2000
                return O00OOOO00OO0OO0O0 ['params']#line:2001
            elif O0OO0O00000O0OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:2002
                return O00OOOO00OO0OO0O0 ['params']#line:2003
            elif O0OO0O00000O0OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:2004
                return O00OOOO00OO0OO0O0 ['params']#line:2005
            else :#line:2006
                print ("Unsupported task type for rule details")#line:2007
        else :#line:2008
            print ("No such rule.")#line:2009
    def get_varlist (OO0OOOO00O0OOOOOO ):#line:2011
        return OO0OOOO00O0OOOOOO .result ["datalabels"]["varname"]#line:2012
    def get_category_names (O00OOOOOOO00OO00O ,varname =None ,varindex =None ):#line:2014
        OO0O00O0OO0O0O00O =0 #line:2015
        if varindex is not None :#line:2016
            if OO0O00O0OO0O0O00O >=0 &OO0O00O0OO0O0O00O <len (O00OOOOOOO00OO00O .get_varlist ()):#line:2017
                OO0O00O0OO0O0O00O =varindex #line:2018
            else :#line:2019
                print ("Error: no such variable.")#line:2020
                return #line:2021
        if (varname is not None ):#line:2022
            O0OO000O0OOO00000 =O00OOOOOOO00OO00O .get_varlist ()#line:2023
            OO0O00O0OO0O0O00O =O0OO000O0OOO00000 .index (varname )#line:2024
            if OO0O00O0OO0O0O00O ==-1 |OO0O00O0OO0O0O00O <0 |OO0O00O0OO0O0O00O >=len (O00OOOOOOO00OO00O .get_varlist ()):#line:2025
                print ("Error: no such variable.")#line:2026
                return #line:2027
        return O00OOOOOOO00OO00O .result ["datalabels"]["catnames"][OO0O00O0OO0O0O00O ]#line:2028
    def print_data_definition (O0O00O0O00OOOO00O ):#line:2030
        O0OO000OOO0OO00OO =O0O00O0O00OOOO00O .get_varlist ()#line:2031
        for O0O0OO000O00O0O0O in O0OO000OOO0OO00OO :#line:2032
            O000000O0O0O00OOO =O0O00O0O00OOOO00O .get_category_names (O0O0OO000O00O0O0O )#line:2033
            OO000000OO0OO00O0 =""#line:2034
            for OO000O0OOOOOOO00O in O000000O0O0O00OOO :#line:2035
                OO000000OO0OO00O0 =OO000000OO0OO00O0 +str (OO000O0OOOOOOO00O )+" "#line:2036
            OO000000OO0OO00O0 =OO000000OO0OO00O0 [:-1 ]#line:2037
            print (f"Variable {O0O0OO000O00O0O0O} has {len(O0OO000OOO0OO00OO)} categories: {OO000000OO0OO00O0}")#line:2038
    def _is_calculated (OOOO0OO00OOO00000 ):#line:2040
        ""#line:2045
        O0O0O0O0OO0O0O0O0 =False #line:2046
        if 'taskinfo'in OOOO0OO00OOO00000 .result :#line:2047
            O0O0O0O0OO0O0O0O0 =True #line:2048
        return O0O0O0O0OO0O0O0O0 