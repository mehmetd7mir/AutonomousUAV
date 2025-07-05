//
//  AlertAction.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 5.07.2025.
//

import Foundation
import UIKit

struct AlertActionModel {
    let titleKey : String
    let style : UIAlertAction.Style
    let handler : ( () -> Void )?
    let accessibilityHintKey : String?
    let accessibilityLabelKey : String?
    let accessibilityTraits : UIAccessibilityTraits?
}
