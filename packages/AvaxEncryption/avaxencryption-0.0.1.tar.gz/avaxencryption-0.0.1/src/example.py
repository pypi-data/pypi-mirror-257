def avax_encryption(str):
    translation = ""
    for letter in str:
        if letter in "Ss":
            translation = translation + "a"                
        elif letter in "Ww":                                         
            translation = translation + "b"                       
        elif letter in "Xx":                                  
            translation = translation + "c"                 
        elif letter in "Zz":                               
            translation = translation + "d"              
        elif letter in "Bb":                                 
            translation = translation + "e"      
        elif letter in "Pp":              
            translation = translation + "f"               
        elif letter in "Qq":              
            translation = translation + "g"                 
        elif letter in "Ee":                      
            translation = translation + "h"                  
        elif letter in "Ll":      
            translation = translation + "i"            
        elif letter in "Rr":             
            translation = translation + "j"              
        elif letter in "Uu":      
            translation = translation + "k"              
        elif letter in "Dd":               
            translation = translation + "l"                
        elif letter in "Oo":             
            translation = translation + "m"                
        elif letter in "Aa":    
            translation = translation + "n"                    
        elif letter in "Nn":          
            translation = translation + "o"
        elif letter in "Tt":                   
            translation = translation + "p" 
        elif letter in "Hh":                
            translation = translation + "q" 
        elif letter in "Mm":            
            translation = translation + "r"
        elif letter in "Cc":             
            translation = translation + "s"   
        elif letter in "Gg":                    
            translation = translation + "t"
        elif letter in "Ff":                      
            translation = translation + "u"
        elif letter in "Jj":             
            translation = translation + "v"
        elif letter in "Yy":                      
            translation = translation + "w"
        elif letter in "Kk":                      
            translation = translation + "x"
        elif letter in "Vv":                          
            translation = translation + "y"
        elif letter in "Ii":                            
            translation = translation + "z"   
        elif letter in "1":                
            translation = translation + "*"
        elif letter in "2":                            
            translation = translation + "!"    
        elif letter in "3":                            
            translation = translation + ">" 
        elif letter in "4":                            
            translation = translation + "$" 
        elif letter in "5":                            
            translation = translation + "&" 
        elif letter in "6":                            
            translation = translation + "#" 
        elif letter in "7":                            
            translation = translation + "@" 
        elif letter in "8":                            
            translation = translation + ")" 
        elif letter in "9":                            
            translation = translation + "="  
        elif letter in "0":                  
            translation = translation + "-"            
        else:                            
            translation = translation + letter 
    return translation
#~-------------Decode function---------------    
def Decrypt_avax(str):
    translation = ""
    for letter in str:
        if letter in "Aa":
            translation = translation + "s"
        elif letter in "Bb":                                          
            translation = translation + "w"                       
        elif letter in "Cc":                            
            translation = translation + "x"                 
        elif letter in "Dd":                                 
            translation = translation + "z"              
        elif letter in "Ee":                                    
            translation = translation + "b"      
        elif letter in "Ff":                 
            translation = translation + "p"               
        elif letter in "Gg":                       
            translation = translation + "q"              
        elif letter in "Hh":                                    
            translation = translation + "e"                       
        elif letter in "Ii":                           
            translation = translation + "l"          
        elif letter in "Jj":                        
            translation = translation + "r"             
        elif letter in "Kk":                         
            translation = translation + "u"            
        elif letter in "Ll":                           
            translation = translation + "d"                
        elif letter in "Mm":                        
            translation = translation + "o"                
        elif letter in "Nn":                     
            translation = translation + "a"                    
        elif letter in "Oo":                     
            translation = translation + "n"
        elif letter in "Pp":                      
            translation = translation + "t"  
        elif letter in "Qq":                    
            translation = translation + "h" 
        elif letter in "Rr":                     
            translation = translation + "m"
        elif letter in "Ss":                 
            translation = translation + "c"  
        elif letter in "Tt":                   
            translation = translation + "g"
        elif letter in "Uu":                    
            translation = translation + "f"
        elif letter in "Vv":                      
            translation = translation + "j" 
        elif letter in "Ww":                        
            translation = translation + "y"  
        elif letter in "Xx":                     
            translation = translation + "k" 
        elif letter in "Yy":                      
            translation = translation + "v"
        elif letter in "Zz":                            
            translation = translation + "i"   
        elif letter in "1":                       
            translation = translation + "*"
        elif letter in "2":                            
            translation = translation + "!"    
        elif letter in "3":                            
            translation = translation + ">" 
        elif letter in "4":                            
            translation = translation + "$" 
        elif letter in "5":                            
            translation = translation + "&" 
        elif letter in "6":                            
            translation = translation + "#" 
        elif letter in "7":                            
            translation = translation + "@" 
        elif letter in "8":                            
            translation = translation + ")" 
        elif letter in "9":                            
            translation = translation + "="  
        elif letter in "0":                            
            translation = translation + "-"              
        else:
            translation = translation + letter
    return translation
