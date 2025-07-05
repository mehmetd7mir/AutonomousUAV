//
//  AlertModel.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 5.07.2025.
//

import Foundation
import UIKit

struct AlertModel {
    let titleKey : String
    let messageKey : String
    let actions : [AlertActionModel]
    let accessibilityHintKey: String?
    let accessibilityLabelKey : String?
    let accessibilityTraits : UIAccessibilityTraits?
    let style: UIAlertController.Style
}
