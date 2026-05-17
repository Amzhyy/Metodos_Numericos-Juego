using TMPro;
using UnityEngine;

/// <summary>
/// Genera colliders en objetos con malla que aún no tienen uno.
/// </summary>
public class SceneCollisionBuilder : MonoBehaviour
{
    [SerializeField] float minColliderSize = 0.05f;

    public int BuildColliders()
    {
        int added = 0;
        var player = GameObject.Find("PLayer");

        foreach (var renderer in FindObjectsOfType<MeshRenderer>(true))
        {
            var go = renderer.gameObject;
            if (!ShouldReceiveCollider(go, player))
                continue;

            var box = go.AddComponent<BoxCollider>();
            FitBoxCollider(box, renderer);
            if (box.size.magnitude < minColliderSize)
            {
                if (Application.isPlaying)
                    Destroy(box);
                else
                    DestroyImmediate(box);
                continue;
            }

            added++;
        }

        return added;
    }

    static bool ShouldReceiveCollider(GameObject go, GameObject player)
    {
        if (go.GetComponent<Collider>() != null)
            return false;

        if (go.GetComponent<CharacterController>() != null)
            return false;

        if (go.GetComponent<Camera>() != null || go.GetComponent<Light>() != null)
            return false;

        if (go.GetComponent<Terrain>() != null)
            return false;

        if (go.GetComponent<TextMeshPro>() != null)
            return false;

        if (player != null && (go == player || go.transform.IsChildOf(player.transform)))
            return false;

        return go.GetComponent<MeshFilter>() != null;
    }

    static void FitBoxCollider(BoxCollider box, Renderer renderer)
    {
        var bounds = renderer.bounds;
        var t = renderer.transform;
        box.center = t.InverseTransformPoint(bounds.center);

        var scale = t.lossyScale;
        box.size = new Vector3(
            bounds.size.x / Mathf.Max(Mathf.Abs(scale.x), 0.001f),
            bounds.size.y / Mathf.Max(Mathf.Abs(scale.y), 0.001f),
            bounds.size.z / Mathf.Max(Mathf.Abs(scale.z), 0.001f));
    }
}
