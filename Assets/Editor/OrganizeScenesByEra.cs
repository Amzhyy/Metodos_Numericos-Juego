using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class OrganizeScenesByEra
{
    private static readonly string[] SceneTitles =
    {
        "Auditorio -Epoca Montante",
        "Epoca-Newton",
        "Epoca-Lagrange",
        "Epoca-Gauss",
        "Epoca-Raphson",
    };

    private static readonly HashSet<string> KeepAtRoot = new()
    {
        "Terrain",
        "Main Camera",
        "Main Camera (1)",
        "Main Camera (2)",
        "Directional Light",
        "Directional Light (1)",
        "Directional Light (2)",
        "PLayer",
        "Camara",
        "Visor",
    };

    [MenuItem("Tools/Metodos Numericos/Organizar escenas por epoca")]
    public static void OrganizeActiveScene()
    {
        OrganizeScene(SceneManager.GetActiveScene());
    }

    public static void OrganizeAllConfiguredScenes()
    {
        OrganizeSceneAtPath("Assets/Scene_MN.unity");
    }

    public static void OrganizeSceneMnOnly()
    {
        OrganizeSceneAtPath("Assets/Scene_MN.unity");
        EditorApplication.Exit(0);
    }

    private static void OrganizeSceneAtPath(string path)
    {
        if (!System.IO.File.Exists(path))
            return;

        var scene = EditorSceneManager.OpenScene(path, OpenSceneMode.Single);
        var rootsBefore = scene.GetRootGameObjects().Length;
        OrganizeScene(scene);
        var rootsAfter = scene.GetRootGameObjects().Length;

        if (rootsAfter < 3 && rootsBefore > 10)
        {
            Debug.LogError($"No se guardo {path}: la escena quedo casi vacia ({rootsAfter} raices).");
            return;
        }

        EditorSceneManager.SaveScene(scene);
        Debug.Log($"Escena organizada: {path} ({rootsAfter} objetos raiz)");
    }

    private static void OrganizeScene(Scene scene)
    {
        var labels = FindSceneLabels();
        if (labels.Count == 0)
        {
            Debug.LogWarning($"No se encontraron titulos TMP en {scene.name}.");
            return;
        }

        var folders = EnsureSceneFolders(labels);
        var roots = scene.GetRootGameObjects().ToList();

        foreach (var title in SceneTitles)
        {
            if (!labels.TryGetValue(title, out var label) || !folders.TryGetValue(title, out var folder))
                continue;

            if (label.parent != folder)
                Undo.SetTransformParent(label, folder, "Mover titulo a carpeta de escena");
        }

        foreach (var root in roots)
        {
            if (ShouldKeepAtRoot(root))
                continue;

            if (folders.Values.Contains(root.transform))
                continue;

            var nearest = NearestLabel(root.transform.position, labels);
            if (nearest == null)
                continue;

            var folder = folders[nearest];
            if (root.transform.parent == folder)
                continue;

            Undo.SetTransformParent(root.transform, folder, "Organizar escena por epoca");
        }

        EditorSceneManager.MarkSceneDirty(scene);
    }

    private static Dictionary<string, Transform> FindSceneLabels()
    {
        var result = new Dictionary<string, Transform>();
        foreach (var tmp in Object.FindObjectsOfType<TextMeshPro>(true))
        {
            var text = tmp.text.Trim();
            foreach (var title in SceneTitles)
            {
                if (text.Contains(title) || title.Contains(text))
                {
                    result[title] = tmp.transform;
                    break;
                }
            }
        }

        return result;
    }

    private static Dictionary<string, Transform> EnsureSceneFolders(Dictionary<string, Transform> labels)
    {
        var folders = new Dictionary<string, Transform>();

        foreach (var title in SceneTitles)
        {
            if (!labels.ContainsKey(title))
                continue;

            var existing = GameObject.Find(title);
            if (existing != null)
            {
                folders[title] = existing.transform;
                continue;
            }

            var lagrange = GameObject.Find("EscenarioLagrange");
            if (lagrange != null && title == "Epoca-Lagrange")
            {
                lagrange.name = title;
                folders[title] = lagrange.transform;
                continue;
            }

            var folderGo = new GameObject(title);
            Undo.RegisterCreatedObjectUndo(folderGo, "Crear carpeta de escena");
            folders[title] = folderGo.transform;
        }

        return folders;
    }

    private static string NearestLabel(Vector3 position, Dictionary<string, Transform> labels)
    {
        string best = null;
        var bestDist = float.MaxValue;

        foreach (var pair in labels)
        {
            var labelPos = pair.Value.position;
            var dist = (new Vector2(position.x, position.z) - new Vector2(labelPos.x, labelPos.z)).sqrMagnitude;
            if (dist < bestDist)
            {
                bestDist = dist;
                best = pair.Key;
            }
        }

        return best;
    }

    private static bool ShouldKeepAtRoot(GameObject go)
    {
        if (KeepAtRoot.Contains(go.name))
            return true;

        if (go.GetComponent<Camera>() != null)
            return true;

        if (go.GetComponent<Light>() != null)
            return true;

        if (go.GetComponent<Terrain>() != null)
            return true;

        return false;
    }
}

public static class OrganizeScenesByEraBatch
{
    public static void Run()
    {
        OrganizeScenesByEra.OrganizeAllConfiguredScenes();
        EditorApplication.Exit(0);
    }

    public static void RunSceneMn()
    {
        OrganizeScenesByEra.OrganizeSceneMnOnly();
    }
}
