//
//  AppAlertTemplate.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 5.07.2025.
//

import Foundation

enum AppAlertTemplate {
    case testAlert
}

extension AppAlertTemplate {
    func toModel() -> AlertModel {
        switch self {
        case .testAlert:
            return AlertModel(
                titleKey: "alert.test.title",
                messageKey: "alert.test.message",
                actions: [
                    AlertActionModel(
                        titleKey: "common.ok",
                        style: .default,
                        handler: nil,
                        accessibilityHintKey: "hint.ok",
                        accessibilityLabelKey: "label.ok",
                        accessibilityTraits: .button
                    )
                ],
                accessibilityHintKey: "hint.test_alert",
                accessibilityLabelKey: "label.test_alert",
                accessibilityTraits: .staticText,
                style: .alert
            )
        }
    }
}
