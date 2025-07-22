using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.Networking;

public class RealmAPI : MonoBehaviour
{
    public TMP_Dropdown realmTypeDropdown; // Dropdown for realm types
    public Transform realmListContainer;  // Parent object for realm buttons
    public GameObject realmButtonPrefab;  // Prefab for realm buttons
    private string baseUrl = "http://localhost:5002/realms";

    public void FetchRealmsByType()
    {
        string selectedType = realmTypeDropdown.options[realmTypeDropdown.value].text;
        StartCoroutine(GetRealms(selectedType));
    }

    IEnumerator GetRealms(string realmType)
    {
        string url = string.IsNullOrEmpty(realmType) ? baseUrl : $"{baseUrl}?type={realmType}";
        using (UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"Error fetching realms: {request.error}");
            }
            else
            {
                // Parse JSON response
                var realms = JsonUtility.FromJson<RealmList>(request.downloadHandler.text);
                PopulateRealmList(realms.realms);
            }
        }
    }

    void PopulateRealmList(List<Realm> realms)
    {
        // Clear existing buttons
        foreach (Transform child in realmListContainer)
        {
            Destroy(child.gameObject);
        }

        // Create a button for each realm
        foreach (var realm in realms)
        {
            GameObject button = Instantiate(realmButtonPrefab, realmListContainer);
            button.GetComponentInChildren<TextMeshProUGUI>().text = realm.name;

            // Add functionality to connect to the realm on button click
            button.GetComponent<Button>().onClick.AddListener(() =>
            {
                ConnectToRealm(realm.ip_address, realm.port);
            });
        }
    }

    void ConnectToRealm(string ipAddress, int port)
    {
        Debug.Log($"Connecting to realm: {ipAddress}:{port}");
        // TODO: Implement realm connection logic
    }
}

// Helper classes for JSON parsing
[System.Serializable]
public class Realm
{
    public int id;
    public string name;
    public string type;
    public string ip_address;
    public int port;
    public bool is_online;
    public int max_players;
    public int current_players;
}

[System.Serializable]
public class RealmList
{
    public List<Realm> realms;
}
