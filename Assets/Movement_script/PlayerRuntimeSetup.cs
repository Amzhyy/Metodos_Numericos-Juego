using UnityEngine;

/// <summary>
/// Al iniciar Play: activa solo la camara del jugador y desactiva el resto.
/// </summary>
[DefaultExecutionOrder(-200)]
public class PlayerRuntimeSetup : MonoBehaviour
{
    void Awake()
    {
        var player = GameObject.Find("PLayer");
        if (player == null)
            return;

        var playerCamera = player.transform.Find("Camara")?.GetComponent<Camera>();
        if (playerCamera == null)
            return;

        foreach (var cam in FindObjectsOfType<Camera>(true))
        {
            if (cam == playerCamera)
                continue;

            cam.enabled = false;
            cam.gameObject.SetActive(false);
        }

        playerCamera.gameObject.SetActive(true);
        playerCamera.enabled = true;
        playerCamera.tag = "MainCamera";

        var listeners = FindObjectsOfType<AudioListener>(true);
        foreach (var listener in listeners)
            listener.enabled = listener.gameObject == playerCamera.gameObject;

        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }
}
