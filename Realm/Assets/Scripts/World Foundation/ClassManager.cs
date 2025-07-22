using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class ClassManager : MonoBehaviour
{
    [System.Serializable]
    public class ClassData
    {
        public string className; // Name of the class
        public bool isUnlocked; // Whether the class is unlocked
        public Button classButton; // Button associated with this class
        public GameObject classUIPanel; // Panel associated with this class
        public bool isInitialized; // Tracks if the button has been initialized
    }

    [Header("Class Settings")]
    [SerializeField] private List<ClassData> classes; // List of all classes

    private GameObject currentActivePanel; // The currently active class panel

    private void Start()
    {
        // Initialize all buttons and panels
        foreach (var classData in classes)
        {
            InitializeClassButton(classData);
        }
    }

    private void InitializeClassButton(ClassData classData)
    {
        if (classData.isInitialized || classData.classButton == null)
        {
            Debug.LogWarning($"Skipping initialization for {classData.className}: Already initialized or missing Button.");
            return;
        }

        TMP_Text buttonText = classData.classButton.GetComponentInChildren<TMP_Text>();
        TooltipTrigger tooltipTrigger = classData.classButton.GetComponent<TooltipTrigger>();

        if (tooltipTrigger == null)
        {
            tooltipTrigger = classData.classButton.gameObject.AddComponent<TooltipTrigger>();
        }

        // Set button appearance
        buttonText.text = classData.className;
        buttonText.color = classData.isUnlocked ? Color.white : Color.gray;
        classData.classButton.interactable = classData.isUnlocked;

        // Update tooltip state
        tooltipTrigger.SetLockedState(!classData.isUnlocked);

        // Assign button functionality
        classData.classButton.onClick.RemoveAllListeners();
        classData.classButton.onClick.AddListener(() => OnClassSelected(classData));

        classData.isInitialized = true; // Mark as initialized
    }

    private void OnClassSelected(ClassData selectedClass)
    {
        if (!selectedClass.isUnlocked)
        {
            Debug.LogWarning($"Class {selectedClass.className} is locked!");
            return;
        }

        // Deactivate the current panel
        if (currentActivePanel != null)
        {
            currentActivePanel.SetActive(false);
        }

        // Activate the new panel
        if (selectedClass.classUIPanel != null)
        {
            currentActivePanel = selectedClass.classUIPanel;
            currentActivePanel.SetActive(true);
        }
        else
        {
            Debug.LogWarning($"Class {selectedClass.className} has no associated UI panel.");
        }
    }

    public void UnlockClass(string className)
    {
        foreach (var classData in classes)
        {
            if (classData.className == className)
            {
                if (!classData.isUnlocked)
                {
                    classData.isUnlocked = true;

                    // Update tooltip trigger state
                    TooltipTrigger tooltipTrigger = classData.classButton.GetComponent<TooltipTrigger>();
                    if (tooltipTrigger != null)
                    {
                        tooltipTrigger.SetLockedState(false);
                    }

                    Debug.Log($"Class {className} is now unlocked!");
                }
                else
                {
                    Debug.Log($"Class {className} is already unlocked.");
                }
                break;
            }
        }
    }
}
