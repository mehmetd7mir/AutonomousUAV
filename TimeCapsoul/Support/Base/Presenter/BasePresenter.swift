//
//  BasePresenter.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 23.06.2025.
//

import Foundation

public protocol BasePresenter: AnyObject {
    associatedtype View: BaseView & AnyObject  //must be weak : associatedtype View allows us to keep the presenter generic and reusable.

    var view: View? { get set } // must be weak

    init(view: View)

    func viewDidLoad()
    func viewWillAppear()
    func viewDidAppear()
    func viewWillDisappear()
    func viewDidDisappear()
}




/* Learning
       
                    *?* -ASSOCIATEDTYPE & TYPEALIES *?*
   
   In swift we use they for that when we use a some type but we dont know exactly except one of its feature.Let think about it with example;
   Let's say there is a tv show.A singer is coming every episode.We dont know who is this singer but we know a singer comes every episode and singSong().
 
   protocol tvShow {
        associatedtype Guest : Singer // Comed person is a singer but we dont know who is person ?
        var currentEpisodeGuest : Guest? {get set}
        func singSong()
   }
 
 -> then anybody comes and use this protocol
 
   struct swiftShow : tvShow {
        typealias Guest = EnginNursani
        var currentEpisodeGuest = EnginNursani?
 
      func singSong(){
        currentEpisodeGuest?.sing()
      }
   }

   protocol Singer {
     func sing()
   }
   struct EnginNursani : Singer {
     func sing() {
         print("Bu dunyada yalnız kaldım.")
     }
   }
   
        
 
*/
