using UnityEngine;
using UnityEngine.EventSystems;

public class TooltipTrigger : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    [Header("Tooltip Prefabs")]
    public GameObject lockedTooltipPrefab;
    public GameObject unlockedTooltipPrefab;

    [Header("State")]
    public bool isLocked = true; // Default state

    private GameObject tooltipInstance; // The active tooltip instance
    private const string StateKeyPrefix = "TooltipState_"; // Prefix for PlayerPrefs key

    private string StateKey => StateKeyPrefix + gameObject.name; // Unique key for this tooltip state

    private void Start()
    {
        LoadState();
    }

    public void SetLockedState(bool locked)
    {
        isLocked = locked;
        SaveState();
    }

    private void SaveState()
    {
        PlayerPrefs.SetInt(StateKey, isLocked ? 1 : 0);
        PlayerPrefs.Save();
    }

    private void LoadState()
    {
        if (PlayerPrefs.HasKey(StateKey))
        {
            isLocked = PlayerPrefs.GetInt(StateKey) == 1;
        }
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        if (tooltipInstance == null)
        {
            GameObject prefab = isLocked ? lockedTooltipPrefab : unlockedTooltipPrefab;

            if (prefab != null)
            {
                tooltipInstance = Instantiate(prefab, transform.position, Quaternion.identity, transform.parent);
            }
        }
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        if (tooltipInstance != null)
        {
            Destroy(tooltipInstance);
            tooltipInstance = null;
        }
    }
}
