using UnityEngine;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

[RequireComponent(typeof(CharacterController))]
public class FirstPersonPlayer : MonoBehaviour
{
    [Header("Movimiento")]
    [SerializeField] float walkSpeed = 6f;
    [SerializeField] float sprintSpeed = 10f;
    [SerializeField] float gravity = -28f;
    [SerializeField] float jumpHeight = 1.4f;

    [Header("Camara")]
    [SerializeField] Transform cameraPivot;
    [SerializeField] float mouseSensitivity = 2f;
    [SerializeField] float minPitch = -85f;
    [SerializeField] float maxPitch = 85f;

    CharacterController controller;
    float pitch;
    Vector3 verticalVelocity;

    void Awake()
    {
        controller = GetComponent<CharacterController>();
        if (cameraPivot == null)
            cameraPivot = transform.Find("Camara");

        var bodyRenderer = GetComponent<MeshRenderer>();
        if (bodyRenderer != null)
            bodyRenderer.enabled = false;
    }

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;

        if (cameraPivot != null)
        {
            cameraPivot.localRotation = Quaternion.identity;
            var cam = cameraPivot.GetComponent<Camera>();
            if (cam != null)
            {
                cam.enabled = true;
                cam.tag = "MainCamera";
            }
        }
    }

    void Update()
    {
        HandleLook();
        HandleMove();
    }

    void HandleLook()
    {
        Vector2 look = ReadLookDelta();
        float yaw = look.x * mouseSensitivity;
        float pitchDelta = look.y * mouseSensitivity;

        transform.Rotate(Vector3.up, yaw, Space.World);

        pitch -= pitchDelta;
        pitch = Mathf.Clamp(pitch, minPitch, maxPitch);

        if (cameraPivot != null)
            cameraPivot.localRotation = Quaternion.Euler(pitch, 0f, 0f);
    }

    void HandleMove()
    {
        Vector2 input = ReadMoveInput();
        Vector3 move = transform.right * input.x + transform.forward * input.y;
        if (move.sqrMagnitude > 1f)
            move.Normalize();

        float speed = IsSprinting() ? sprintSpeed : walkSpeed;
        controller.Move(move * speed * Time.deltaTime);

        if (controller.isGrounded && verticalVelocity.y < 0f)
            verticalVelocity.y = -2f;

        if (controller.isGrounded && IsJumpPressed())
            verticalVelocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);

        verticalVelocity.y += gravity * Time.deltaTime;
        controller.Move(verticalVelocity * Time.deltaTime);
    }

    static Vector2 ReadMoveInput()
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            float x = 0f;
            float y = 0f;
            if (Keyboard.current.aKey.isPressed || Keyboard.current.leftArrowKey.isPressed) x -= 1f;
            if (Keyboard.current.dKey.isPressed || Keyboard.current.rightArrowKey.isPressed) x += 1f;
            if (Keyboard.current.sKey.isPressed || Keyboard.current.downArrowKey.isPressed) y -= 1f;
            if (Keyboard.current.wKey.isPressed || Keyboard.current.upArrowKey.isPressed) y += 1f;
            if (x != 0f || y != 0f)
                return new Vector2(x, y).normalized;
        }
#endif
        return new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
    }

    static bool IsSprinting()
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
            return Keyboard.current.leftShiftKey.isPressed;
#endif
        return Input.GetKey(KeyCode.LeftShift);
    }

    static bool IsJumpPressed()
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
            return Keyboard.current.spaceKey.wasPressedThisFrame;
#endif
        return Input.GetButtonDown("Jump");
    }

    static Vector2 ReadLookDelta()
    {
#if ENABLE_INPUT_SYSTEM
        if (Mouse.current != null)
            return Mouse.current.delta.ReadValue() * 0.1f;
#endif
        return new Vector2(Input.GetAxis("Mouse X"), Input.GetAxis("Mouse Y"));
    }
}
