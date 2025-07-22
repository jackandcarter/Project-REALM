# Realm Unity Project

This folder contains the Unity client for Project REALM.

## Unity Version
The project was created with **Unity 6000.0.34f1** as shown in `ProjectSettings/ProjectVersion.txt`. Make sure this version is installed in Unity Hub before opening the project.

## Opening the Project in Unity Hub
1. Start **Unity Hub**.
2. Click **Add** and choose this `Realm` directory.
3. When prompted, select **6000.0.34f1** as the Unity version.

## Available Scenes
The following scenes are available in `Assets`:
- `MainMenu.unity`
- `Elysium.unity`
- `OutdoorsScene.unity`

The Digger plugin also provides demo scenes under `Assets/Digger/Demo`:
- `Simple Scene/simple-scene.unity`
- `Runtime Scene/runtime-scene.unity`

## Digger Plugin
The terrain editing plugin **Digger** is located in `Assets/Digger`.
According to `Assets/Digger/README.txt`, it requires the **Burst** package and, for Digger Pro, also **AI Navigation**:
1. Open **Window > Package Manager**.
2. Install **Burst** (and **AI Navigation** if using Digger Pro).
After installation the menu **Tools > Digger** becomes available.
