using UnityEngine;
using UnityEngine.SceneManagement;

/// <summary>
/// Controla la lógica del Menú Principal del Escape Room Numérico.
/// Asignar este script a un GameObject vacío llamado "MainMenuManager" en la escena del menú.
/// </summary>
public class MainMenuManager : MonoBehaviour
{
    [Header("Configuración de Escenas")]
    [Tooltip("Nombre exacto de la escena del juego (Build Settings)")]
    [SerializeField] private string gameSceneName = "Scene_MN";

    [Header("Animación de Botones (Opcional)")]
    [Tooltip("Duración de la animación de salida antes de cargar la escena")]
    [SerializeField] private float transitionDelay = 0.5f;

    // ─────────────────────────────────────────────────────────────────────────
    //  BOTÓN INICIAR
    // ─────────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Llamar desde el evento OnClick() del botón "INICIAR".
    /// Carga la escena principal del juego.
    /// </summary>
    public void OnIniciarPressed()
    {
        Debug.Log("[MainMenu] INICIAR presionado — Cargando escena: " + gameSceneName);
        // Opcional: reproducir sonido / animación de salida aquí
        StartCoroutine(LoadGameWithDelay());
    }

    private System.Collections.IEnumerator LoadGameWithDelay()
    {
        // Aquí puedes activar un animator / fade-out antes de cambiar escena
        yield return new WaitForSeconds(transitionDelay);
        SceneManager.LoadScene(gameSceneName);
    }

    // ─────────────────────────────────────────────────────────────────────────
    //  BOTÓN SALIR
    // ─────────────────────────────────────────────────────────────────────────

    /// <summary>
    /// Llamar desde el evento OnClick() del botón "SALIR".
    /// Cierra la aplicación (en Editor solo detiene el Play Mode).
    /// </summary>
    public void OnSalirPressed()
    {
        Debug.Log("[MainMenu] SALIR presionado — Cerrando aplicación.");

#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
}
