using UnityEngine;

/// <summary>
/// Anima el orbe/giroscopio central del menú:
/// rotación continua + pulso de luz azul.
/// Adjuntar al GameObject del orbe (el aro giratorio del centro).
/// </summary>
public class OrbAnimator : MonoBehaviour
{
    [Header("Rotación")]
    [SerializeField] private float rotationSpeedX = 20f;
    [SerializeField] private float rotationSpeedY = 35f;
    [SerializeField] private float rotationSpeedZ = 10f;

    [Header("Pulso de emisión (Material)")]
    [Tooltip("Material que tiene la propiedad _EmissionColor")]
    [SerializeField] private Renderer orbRenderer;
    [SerializeField] private Color    emissionMin = new Color(0.0f, 0.3f, 0.8f);
    [SerializeField] private Color    emissionMax = new Color(0.1f, 0.7f, 1.0f);
    [SerializeField] private float    pulseSpeed  = 1.5f;

    void Update()
    {
        // Rotación continua
        transform.Rotate(rotationSpeedX * Time.deltaTime,
                         rotationSpeedY * Time.deltaTime,
                         rotationSpeedZ * Time.deltaTime,
                         Space.Self);

        // Pulso de emisión
        if (orbRenderer != null)
        {
            float t = (Mathf.Sin(Time.time * pulseSpeed) + 1f) * 0.5f;
            Color emission = Color.Lerp(emissionMin, emissionMax, t);
            orbRenderer.material.SetColor("_EmissionColor", emission);
        }
    }
}
