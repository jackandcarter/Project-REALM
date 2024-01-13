using UnityEngine;
using UnityEngine.UI;

public class RealmListItem : MonoBehaviour
{
    public Text realmNameText;
    public Text realmTypeText;
    public Text connectedUsersText;
    public Text characterCountText;

    private RealmManager realmManager;
    private string realmName;

    public void Setup(string name, string type, int connectedUsers, int characterCount, RealmManager manager)
    {
        realmName = name;
        realmNameText.text = "Name: " + name;
        realmTypeText.text = "Type: " + type;
        connectedUsersText.text = "Connected Users: " + connectedUsers.ToString();
        characterCountText.text = "Character Count: " + characterCount.ToString();

        realmManager = manager;
    }

    public void OnRealmItemClick()
    {
        // Notify RealmManager that this realm is selected
        realmManager.OnRealmSelected(realmName);
    }
}
