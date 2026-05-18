using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

/// <summary>
/// Efecto de hover/pulse para los botones del menú con estética golden/dark.
/// Adjuntar a cada GameObject de botón junto a su componente Button.
/// </summary>
[RequireComponent(typeof(Button))]
public class MenuButtonEffect : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerDownHandler, IPointerUpHandler
{
    [Header("Colores del botón")]
    [SerializeField] private Color normalColor    = new Color(0.05f, 0.08f, 0.18f, 0.92f);
    [SerializeField] private Color hoverColor     = new Color(0.08f, 0.14f, 0.30f, 0.97f);
    [SerializeField] private Color pressedColor   = new Color(0.03f, 0.05f, 0.12f, 1.00f);

    [Header("Escala de hover")]
    [SerializeField] private float hoverScale  = 1.04f;
    [SerializeField] private float normalScale = 1.00f;
    [SerializeField] private float scaleSpeed  = 8f;

    [Header("Glow image (opcional)")]
    [Tooltip("Imagen interior del borde dorado para animar su alpha")]
    [SerializeField] private Image glowImage;

    private Image       _bg;
    private RectTransform _rt;
    private float       _targetScale;
    private Color       _targetColor;
    private float       _glowAlpha;

    void Awake()
    {
        _bg          = GetComponent<Image>();
        _rt          = GetComponent<RectTransform>();
        _targetScale = normalScale;
        _targetColor = normalColor;

        if (_bg) _bg.color = normalColor;
        if (glowImage) { var c = glowImage.color; c.a = 0f; glowImage.color = c; }
    }

    void Update()
    {
        // Escala suave
        float current = _rt.localScale.x;
        float next    = Mathf.Lerp(current, _targetScale, Time.deltaTime * scaleSpeed);
        _rt.localScale = Vector3.one * next;

        // Color suave
        if (_bg) _bg.color = Color.Lerp(_bg.color, _targetColor, Time.deltaTime * scaleSpeed);

        // Glow suave
        if (glowImage)
        {
            var c = glowImage.color;
            c.a = Mathf.Lerp(c.a, _glowAlpha, Time.deltaTime * scaleSpeed);
            glowImage.color = c;
        }
    }

    public void OnPointerEnter(PointerEventData _)
    {
        _targetScale = hoverScale;
        _targetColor = hoverColor;
        _glowAlpha   = 1f;
    }

    public void OnPointerExit(PointerEventData _)
    {
        _targetScale = normalScale;
        _targetColor = normalColor;
        _glowAlpha   = 0f;
    }

    public void OnPointerDown(PointerEventData _)
    {
        _targetScale = normalScale * 0.97f;
        _targetColor = pressedColor;
    }

    public void OnPointerUp(PointerEventData _)
    {
        _targetScale = hoverScale;
        _targetColor = hoverColor;
    }
}
