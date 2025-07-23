using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

public class CharacterAPI : MonoBehaviour
{
    private string baseUrl = "http://localhost:5003/characters";

    public IEnumerator CreateCharacter(int accountId, string name, int classId, string appearance)
    {
        var payload = JsonUtility.ToJson(new CharacterCreate{ account_id = accountId, name = name, class_id = classId, appearance = appearance });
        using (UnityWebRequest req = new UnityWebRequest(baseUrl, "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(payload);
            req.uploadHandler = new UploadHandlerRaw(bodyRaw);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            yield return req.SendWebRequest();
            Debug.Log($"CreateCharacter response: {req.downloadHandler.text}");
        }
    }

    public IEnumerator GetCharacters(int accountId)
    {
        string url = baseUrl + "/" + accountId;
        using (UnityWebRequest req = UnityWebRequest.Get(url))
        {
            yield return req.SendWebRequest();
            Debug.Log($"Characters: {req.downloadHandler.text}");
        }
    }

    public IEnumerator UpdateCharacter(int charId, int classId, string appearance)
    {
        var payload = JsonUtility.ToJson(new CharacterUpdate{ class_id = classId, appearance = appearance });
        using (UnityWebRequest req = new UnityWebRequest(baseUrl + "/" + charId, "PUT"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(payload);
            req.uploadHandler = new UploadHandlerRaw(bodyRaw);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            yield return req.SendWebRequest();
            Debug.Log($"UpdateCharacter response: {req.downloadHandler.text}");
        }
    }

    public IEnumerator DeleteCharacter(int charId)
    {
        using (UnityWebRequest req = UnityWebRequest.Delete(baseUrl + "/" + charId))
        {
            yield return req.SendWebRequest();
            Debug.Log($"DeleteCharacter response: {req.downloadHandler.text}");
        }
    }

    [System.Serializable]
    private class CharacterCreate
    {
        public int account_id;
        public string name;
        public int class_id;
        public string appearance;
    }

    [System.Serializable]
    private class CharacterUpdate
    {
        public int class_id;
        public string appearance;
    }
}
