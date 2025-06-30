//
//  SupportedLanguage.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 2025-06-23.
//


import Foundation
import UIKit

enum SupportedLanguage : CaseIterable {
    
    case english
    case turkish
    case german
    case spanish
    case french
    case italian
    case japanese
    case arabic
    
    
    var isoCode: String {
        switch self {
        case .english: return "en"
        case .turkish: return "tr"
        case .german: return "de"
        case .spanish: return "es"
        case .french: return "fr"
        case .italian: return "it"
        case .japanese: return "ja"
        case .arabic: return "ar"
        }
    }
    
    var nativeName: String {
        switch self {
        case .english: return "English"
        case .turkish: return "Türkçe"
        case .german: return "Deutsch"
        case .spanish: return "Español"
        case .french: return "Français"
        case .italian: return "Italiano"
        case .japanese: return "日本語"
        case .arabic: return "العربية"
        }
    }
    
    var localizedName : String {
        let key = "language.\(isoCode)"
        return key.localized
    }
    
    var locale : Locale {
        Locale(identifier: isoCode)
    }
    
    static let `default`: SupportedLanguage = .english
}

extension SupportedLanguage {
    var flagName : UIImage? {
        return UIImage(named : isoCode)
    }
}
