//
//  String+Localized.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 2025-06-23.

import Foundation

extension String {
    
    var localized : String {
        
        // the word is "self" in here
        // NSLocalizedString("language.tr" , comment : "" )  will be "language.tr".localized
        
        NSLocalizedString(
            self,
            tableName: nil, // it is name of .strings file : comfortable for scabilityte
            bundle: LanguageManager.shared.activeBundle, // determines using which "lproj" file, it comes from our localizedmanager.shared
            value : "[Missing **\(self)** ]",
            comment: ""
        )
        
    }
    
    
    // if there is a number or variable in string we will use this func.
    func localized(with arguments : CVarArg...) -> String {
        
        String(format : self.localized, arguments: arguments)
        
        // let name = "md7"
        // let message = "welcome.message".localized(with : name)
        // print(message)
        
    }
    
}


/* Learning
 
 CVarArg : Duty of this protocol is to harmonise things in C language for example printf()
 we can more than one parameter with "..."

 */
