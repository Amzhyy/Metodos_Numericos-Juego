using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Move : MonoBehaviour
{
    [SerializeField] float sensibilidad = 100f;
    public Transform Player;

    float rotacionvertical = 0f;

    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
    }

    void Update()
    {
        float mouseX = Input.GetAxis("Mouse X") * sensibilidad * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * sensibilidad * Time.deltaTime;

        
        rotacionvertical -= mouseY;
        rotacionvertical = Mathf.Clamp(rotacionvertical, -90f, 90f);

        transform.localRotation = Quaternion.Euler(rotacionvertical, 0f, 0f);

        
        Player.Rotate(Vector3.up * mouseX);
    }
}