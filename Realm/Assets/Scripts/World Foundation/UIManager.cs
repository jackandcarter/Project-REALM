using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class UIManager : MonoBehaviour
{
    [System.Serializable]
    public class DropdownPanel
    {
        public string panelName; // Name of the panel
        public Button triggerButton; // Button that triggers this dropdown
        public GameObject panelObject; // The panel to toggle
    }

    [Header("Dropdown Panels")]
    [SerializeField] private List<DropdownPanel> dropdownPanels; // List of all dropdown panels
    [SerializeField] private GameObject overlayClickArea; // Transparent overlay to detect outside clicks

    private GameObject currentOpenPanel; // The currently open dropdown panel
    private bool isHoldingButton = false; // Tracks if the button is held

    private void Start()
    {
        // Set up button listeners for each dropdown panel
        foreach (var dropdown in dropdownPanels)
        {
            if (dropdown.triggerButton != null && dropdown.panelObject != null)
            {
                // Add click behavior
                dropdown.triggerButton.onClick.AddListener(() => ToggleDropdownPanel(dropdown.panelObject));

                // Add hold-to-open behavior
                EventTrigger eventTrigger = dropdown.triggerButton.gameObject.AddComponent<EventTrigger>();

                EventTrigger.Entry pointerDownEntry = new EventTrigger.Entry
                {
                    eventID = EventTriggerType.PointerDown
                };
                pointerDownEntry.callback.AddListener((eventData) => OpenDropdownOnHold(dropdown.panelObject));
                eventTrigger.triggers.Add(pointerDownEntry);

                EventTrigger.Entry pointerUpEntry = new EventTrigger.Entry
                {
                    eventID = EventTriggerType.PointerUp
                };
                pointerUpEntry.callback.AddListener((eventData) => CloseDropdownOnRelease());
                eventTrigger.triggers.Add(pointerUpEntry);
            }
        }

        // Ensure the overlay is hidden by default
        if (overlayClickArea != null)
        {
            overlayClickArea.SetActive(false);
            Button overlayButton = overlayClickArea.GetComponent<Button>();
            if (overlayButton != null)
            {
                overlayButton.onClick.AddListener(CloseAllPanels);
            }
        }
    }

    public void ToggleDropdownPanel(GameObject panelToToggle)
    {
        // Close the panel if it's already open
        if (currentOpenPanel == panelToToggle)
        {
            CloseAllPanels();
            return;
        }

        // Close any currently open panel
        CloseAllPanels();

        // Open the new panel
        panelToToggle.SetActive(true);
        currentOpenPanel = panelToToggle;

        // Activate the overlay for outside click detection
        if (overlayClickArea != null)
        {
            overlayClickArea.SetActive(true);
        }
    }

    public void CloseAllPanels()
    {
        // Close all dropdown panels
        foreach (var dropdown in dropdownPanels)
        {
            dropdown.panelObject.SetActive(false);
        }

        currentOpenPanel = null;

        // Deactivate the overlay
        if (overlayClickArea != null)
        {
            overlayClickArea.SetActive(false);
        }
    }

    private void OpenDropdownOnHold(GameObject panelToToggle)
    {
        isHoldingButton = true;
        panelToToggle.SetActive(true);
        currentOpenPanel = panelToToggle;
    }

    private void CloseDropdownOnRelease()
    {
        if (isHoldingButton)
        {
            isHoldingButton = false;
            if (currentOpenPanel != null)
            {
                currentOpenPanel.SetActive(false);
                currentOpenPanel = null;

                // Deactivate the overlay if it was used
                if (overlayClickArea != null)
                {
                    overlayClickArea.SetActive(false);
                }
            }
        }
    }
}
