using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class SetupGameplay
{
    private const string PlayerObjectName = "PLayer";
    private const string GameplaySystemsName = "GameplaySystems";
    private const string CameraChildName = "Camara";

    // Escala del escenario (props ~3x); jugador ~2.8 m
    private const float PlayerHeight = 2.8f;
    private const float PlayerRadius = 0.42f;
    private const float EyeHeight = 2.35f;
    private static readonly Vector3 SpawnPosition = new(108f, 0.5f, 38f);

    [MenuItem("Tools/Metodos Numericos/Configurar jugador y colisiones")]
    public static void SetupActiveScene()
    {
        SetupCurrentScene();
        EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());
    }

    public static void SetupCurrentScene()
    {
        SetupPlayer();
        DisableExtraCameras();
        EnsureGameplaySystems();
        var added = Object.FindObjectOfType<SceneCollisionBuilder>().BuildColliders();
        Debug.Log($"Colisiones añadidas en {SceneManager.GetActiveScene().name}: {added}");
    }

    static void SetupPlayer()
    {
        var player = GameObject.Find(PlayerObjectName);
        if (player == null)
        {
            Debug.LogWarning("No se encontró el objeto PLayer en la escena.");
            return;
        }

        if (!TagExists("Player"))
            AddTag("Player");

        player.tag = "Player";
        player.transform.position = SpawnPosition;
        player.transform.rotation = Quaternion.identity;
        player.transform.localScale = Vector3.one;

        foreach (var col in player.GetComponents<CapsuleCollider>())
            Object.DestroyImmediate(col);

        var bodyRenderer = player.GetComponent<MeshRenderer>();
        if (bodyRenderer != null)
            bodyRenderer.enabled = false;

        var controller = player.GetComponent<CharacterController>();
        if (controller == null)
            controller = Undo.AddComponent<CharacterController>(player);

        controller.height = PlayerHeight;
        controller.radius = PlayerRadius;
        controller.center = new Vector3(0f, PlayerHeight * 0.5f, 0f);
        controller.slopeLimit = 45f;
        controller.stepOffset = 0.4f;
        controller.skinWidth = 0.08f;

        var oldMove = player.GetComponent<PlayerLocomotion>();
        if (oldMove != null)
            Object.DestroyImmediate(oldMove);

        var fps = player.GetComponent<FirstPersonPlayer>();
        if (fps == null)
            fps = Undo.AddComponent<FirstPersonPlayer>(player);

        var cameraTransform = player.transform.Find(CameraChildName);
        if (cameraTransform != null)
        {
            cameraTransform.localPosition = new Vector3(0f, EyeHeight, 0f);
            cameraTransform.localRotation = Quaternion.identity;
            cameraTransform.localScale = Vector3.one;

            var moveOnCam = cameraTransform.GetComponent<Move>();
            if (moveOnCam != null)
                Object.DestroyImmediate(moveOnCam);

            var cam = cameraTransform.GetComponent<Camera>();
            if (cam != null)
            {
                cam.enabled = true;
                cam.tag = "MainCamera";
                cam.fieldOfView = 70f;
                cam.nearClipPlane = 0.08f;
            }

            var listener = cameraTransform.GetComponent<AudioListener>();
            if (listener != null)
                listener.enabled = true;

            var so = new SerializedObject(fps);
            so.FindProperty("cameraPivot").objectReferenceValue = cameraTransform;
            so.ApplyModifiedPropertiesWithoutUndo();
        }
    }

    static void DisableExtraCameras()
    {
        var playerCamera = GameObject.Find("PLayer/Camara")?.GetComponent<Camera>();
        foreach (var cam in Object.FindObjectsOfType<Camera>(true))
        {
            if (cam == playerCamera)
                continue;

            cam.enabled = false;
            cam.gameObject.SetActive(false);
            var listener = cam.GetComponent<AudioListener>();
            if (listener != null)
                listener.enabled = false;
        }
    }

    static void EnsureGameplaySystems()
    {
        var systems = GameObject.Find(GameplaySystemsName);
        if (systems == null)
        {
            systems = new GameObject(GameplaySystemsName);
            Undo.RegisterCreatedObjectUndo(systems, "Crear GameplaySystems");
        }

        if (systems.GetComponent<SceneCollisionBuilder>() == null)
            Undo.AddComponent<SceneCollisionBuilder>(systems);

        if (systems.GetComponent<PlayerRuntimeSetup>() == null)
            Undo.AddComponent<PlayerRuntimeSetup>(systems);
    }

    static bool TagExists(string tag)
    {
        var asset = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset");
        if (asset == null || asset.Length == 0)
            return false;

        var tagManager = new SerializedObject(asset[0]);
        var tags = tagManager.FindProperty("tags");
        for (int i = 0; i < tags.arraySize; i++)
        {
            if (tags.GetArrayElementAtIndex(i).stringValue == tag)
                return true;
        }

        return false;
    }

    static void AddTag(string tag)
    {
        var asset = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset");
        if (asset == null || asset.Length == 0)
            return;

        var tagManager = new SerializedObject(asset[0]);
        var tags = tagManager.FindProperty("tags");
        for (int i = 0; i < tags.arraySize; i++)
        {
            if (tags.GetArrayElementAtIndex(i).stringValue == tag)
                return;
        }

        tags.InsertArrayElementAtIndex(tags.arraySize);
        tags.GetArrayElementAtIndex(tags.arraySize - 1).stringValue = tag;
        tagManager.ApplyModifiedProperties();
    }
}

public static class SetupGameplayBatch
{
    public static void Run()
    {
        foreach (var path in new[] { "Assets/Scene_MN.unity" })
        {
            if (!System.IO.File.Exists(path))
                continue;

            var scene = EditorSceneManager.OpenScene(path, OpenSceneMode.Single);
            SetupGameplay.SetupCurrentScene();
            EditorSceneManager.SaveScene(scene);
            Debug.Log($"Gameplay configurado: {path}");
        }

        EditorApplication.Exit(0);
    }
}
