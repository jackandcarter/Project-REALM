using System;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class LoginManager : MonoBehaviour
{
    public GameObject loginPanel;
    public GameObject realmListPanel;
    public InputField usernameInput;
    public InputField passwordInput;
    public Text statusText;

    public PlayerManager playerManager;

    private void Start()
    {
        // Show login panel after a defined time (e.g., 5 seconds)
        Invoke("ShowLoginPanel", 5f);
    }

    private void ShowLoginPanel()
    {
        loginPanel.SetActive(true);
    }

    public void OnLoginButtonClick()
    {
        string username = usernameInput.text;
        string password = passwordInput.text;

        StartCoroutine(LoginRequest(username, password));
    }

    private IEnumerator LoginRequest(string username, string password)
    {
        // Use the local IP address or localhost and the port your server is running on
        string loginUrl = "http://localhost:5000/authenticate";

        WWWForm form = new WWWForm();
        form.AddField("username", username);
        form.AddField("password", password);

        using (UnityWebRequest www = UnityWebRequest.Post(loginUrl, form))
        {
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                // Successful login
                Debug.Log("Login Successful");

                // Extract player ID from the response
                int playerId = ExtractPlayerIdFromResponse(www.downloadHandler.text);

                // Pass player ID to PlayerManager
                playerManager.RetainPlayerCredentials(playerId);

                // Close login panel and open the realm list panel
                loginPanel.SetActive(false);
                realmListPanel.SetActive(true);
            }
            else
            {
                // Login failed, handle error
                Debug.LogError("Login Failed: " + www.error);
                statusText.text = "Login Failed: " + www.error;
            }
        }
    }

    private int ExtractPlayerIdFromResponse(string response)
    {
        // Parse the response string to extract the player ID
        if (int.TryParse(response, out int playerId))
        {
            return playerId;
        }
        else
        {
            Debug.LogError("Failed to extract player ID from the response: " + response);
            return -1; // Return a default value or handle the error accordingly
        }
    }
}
