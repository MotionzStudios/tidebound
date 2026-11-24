import Capacitor
import GameKit

@objc(GameCenterPlugin)
public class GameCenterPlugin: CAPPlugin, CAPBridgedPlugin, GKGameCenterControllerDelegate {
    public let identifier = "GameCenterPlugin"
    public let jsName = "GameCenter"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "signIn", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "submitScore", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "showLeaderboards", returnType: CAPPluginReturnPromise)
    ]
    private var authStarted = false

    @objc func signIn(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            let player = GKLocalPlayer.local
            if player.isAuthenticated { call.resolve(["authenticated": true]); return }
            var answered = false
            player.authenticateHandler = { [weak self] vc, error in
                if let vc = vc {
                    self?.bridge?.viewController?.present(vc, animated: true)
                    return
                }
                if answered { return }
                if player.isAuthenticated {
                    answered = true
                    call.resolve(["authenticated": true])
                } else {
                    answered = true
                    call.resolve(["authenticated": false, "error": error?.localizedDescription ?? "not signed in"])
                }
            }
            self.authStarted = true
        }
    }

    @objc func submitScore(_ call: CAPPluginCall) {
        guard GKLocalPlayer.local.isAuthenticated else { call.reject("not authenticated"); return }
        guard let id = call.getString("leaderboardId"),
              let num = call.options["score"] as? NSNumber else { call.reject("bad arguments"); return }
        GKLeaderboard.submitScore(num.intValue, context: 0, player: GKLocalPlayer.local, leaderboardIDs: [id]) { error in
            if let error = error { call.reject(error.localizedDescription) } else { call.resolve() }
        }
    }

    @objc func showLeaderboards(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard GKLocalPlayer.local.isAuthenticated else { call.reject("not authenticated"); return }
            let vc = GKGameCenterViewController(state: .leaderboards)
            vc.gameCenterDelegate = self
            self.bridge?.viewController?.present(vc, animated: true)
            call.resolve()
        }
    }

    public func gameCenterViewControllerDidFinish(_ gameCenterViewController: GKGameCenterViewController) {
        gameCenterViewController.dismiss(animated: true)
    }
}
