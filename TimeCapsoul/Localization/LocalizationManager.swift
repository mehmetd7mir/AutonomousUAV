//
//  LocalizationManager.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 2025-06-23.

import Foundation
import RxSwift
import RxCocoa

final class LanguageManager {
    
    // singleton, no instance
    static let shared = LanguageManager()
    
    var currentLanguage : BehaviorRelay<SupportedLanguage>
    
    // Determines in which language localizable.string files will be read
    var activeBundle : Bundle = .main
    
    private let selectedLanguageKey = "selectedLanguage"
    
    private init() {
        
        if let savedLanguageCode = UserDefaults.standard.string(forKey: selectedLanguageKey),
           let savedLanguage = SupportedLanguage.allCases.first(where : {$0.isoCode == savedLanguageCode }) {
            currentLanguage = BehaviorRelay(value: savedLanguage)
        }
        else {
            currentLanguage = BehaviorRelay(value: SupportedLanguage.default)
        }
        
        updateActiveBundle(for: currentLanguage.value)
        
    }
    
    func setLanguage(_ language: SupportedLanguage) {
        currentLanguage.accept(language)
        UserDefaults.standard.set(language.isoCode, forKey: selectedLanguageKey)
        updateActiveBundle(for: language)
    }
    
    func resetToSystemLanguage() {
        let deviceLanguageCode = Locale.preferredLanguages.first?.components(separatedBy: "-").first ?? "en"
        let systemLanguage = SupportedLanguage.allCases.first(where: {$0.isoCode == deviceLanguageCode }) ?? .default
        setLanguage(systemLanguage)
    }
    
    private func updateActiveBundle(for language: SupportedLanguage) {
        // i should to use safe optional binding because of that swift forced that activeBundle must be String
        // if it is not swift doesn't know what it should does
        if let path = Bundle.main.path(forResource: language.isoCode, ofType: "lproj"),
           let bundle = Bundle(path: path) {
            activeBundle = bundle
        } else {
            activeBundle = .main
        }
    }
    
}

/* Learning
 
 BehaviorRelay<T> is generic.We say that "i have a x object in type T" and it keeps the this object , we can access with listen the changes in x object when it changed.
 
 */
