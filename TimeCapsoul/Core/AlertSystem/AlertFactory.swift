//
//  AlertFactory.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 5.07.2025.
//

import Foundation
import UIKit

final class AlertFactory {
    static func make(from  model : AlertModel) -> UIAlertController {
        let alert = UIAlertController(
            title: model.titleKey.localized,
            message: model.messageKey.localized,
            preferredStyle: model.style
        )
        
        for actionModel in model.actions {
            let action = UIAlertAction(
                title: actionModel.titleKey.localized,
                style: actionModel.style,
                handler: { _ in actionModel.handler?() }
            )
            
            if let hintKey = actionModel.accessibilityHintKey {
                action.accessibilityHint = hintKey.localized
            }
            if let labelKey = actionModel.accessibilityLabelKey {
                action.accessibilityLabel = labelKey.localized
            }
            if let traits = actionModel.accessibilityTraits {
                action.accessibilityTraits = traits
            }
            
            alert.addAction(action)
        }
        if let hintKey = model.accessibilityHintKey {
            alert.view.accessibilityHint = hintKey.localized
        }
        if let labelKey = model.accessibilityLabelKey {
            alert.view.accessibilityLabel = labelKey.localized
        }
        if let traits = model.accessibilityTraits {
            alert.view.accessibilityTraits = traits
        }
        
        UIAccessibility.post(notification: .screenChanged, argument: alert.view)
        
        return alert
    }
}
