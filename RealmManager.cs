using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class RealmManager : MonoBehaviour
{
    public GameObject realmListPanel;
    public GameObject characterListPanel;
    public GameObject characterPreviewPanel;
    public Text defaultChannelText;

    public PlayerManager playerManager;

    public Transform realmListContainer;
    public GameObject realmListItemPrefab;

    private List<RealmInfo> realmList;

    private void Start()
    {
        StartCoroutine(GetRealmsRequest());
    }

    private IEnumerator GetRealmsRequest()
    {
        // Use the local IP address or localhost and the port your realm server is running on
        string getRealmsUrl = "http://localhost:5001/get_realms";

        using (UnityWebRequest www = UnityWebRequest.Get(getRealmsUrl))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                // Parse the JSON response to get the realm list
                realmList = JsonUtility.FromJson<List<RealmInfo>>(www.downloadHandler.text);

                // Populate the realm list UI
                PopulateRealmListUI();

                // Display default channel for the first realm
                if (realmList.Count > 0)
                {
                    StartCoroutine(GetDefaultChannelRequest(realmList[0].name));
                }
            }
            else
            {
                Debug.LogError("Failed to get realms: " + www.error);
            }
        }
    }

    private void PopulateRealmListUI()
    {
        // Instantiate realm list items
        foreach (RealmInfo realmInfo in realmList)
        {
            GameObject realmItem = Instantiate(realmListItemPrefab, realmListContainer);
            RealmListItem realmListItem = realmItem.GetComponent<RealmListItem>();
            realmListItem.Setup(realmInfo.name, realmInfo.type, realmInfo.connected_users, realmInfo.character_count, this);
        }
    }

    public void OnRealmSelected(string realmName)
    {
        // Handle realm selection
        Debug.Log("Realm Selected: " + realmName);

        // Fetch the default channel for the selected realm
        StartCoroutine(GetDefaultChannelRequest(realmName));

        // Transition to Character List Panel
        realmListPanel.SetActive(false);
        characterListPanel.SetActive(true);

        // TODO: Implement character list population and selection logic
    }

    private IEnumerator GetDefaultChannelRequest(string realmName)
    {
        // Use the local IP address or localhost and the port your realm server is running on
        string getDefaultChannelUrl = $"http://localhost:5001/get_default_channel/{realmName}";

        using (UnityWebRequest www = UnityWebRequest.Get(getDefaultChannelUrl))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                string defaultChannel = JsonUtility.FromJson<DefaultChannelResponse>(www.downloadHandler.text).default_channel;

                // Display the default channel in UI (you can update your UI text accordingly)
                defaultChannelText.text = $"Default Channel: {defaultChannel}";
            }
            else
            {
                Debug.LogError("Failed to get default channel: " + www.error);
            }
        }
    }
}

[Serializable]
public class RealmInfo
{
    public string name;
    public string type;
    public int connected_users;
    public int character_count;
}

[Serializable]
public class DefaultChannelResponse
{
    public string default_channel;
}
