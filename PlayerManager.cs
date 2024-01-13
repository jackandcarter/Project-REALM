using UnityEngine;

public class PlayerManager : MonoBehaviour
{
    private int playerId;

    // Retain player credentials
    public void RetainPlayerCredentials(int playerId)
    {
        this.playerId = playerId;
        Debug.Log("Player credentials retained. Player ID: " + playerId);
    }

    // Use this method to access player credentials from other scripts
    public int GetPlayerId()
    {
        return playerId;
    }
}
