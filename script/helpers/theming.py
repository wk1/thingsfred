import os
import shutil

def get_icon_theme():
    """Bestimmt welches Icon-Theme verwendet werden soll"""
    user_theme = os.getenv('icon_theme', 'auto')
    
    # FIX: Check for the actual values from config
    if user_theme == 'Light Icons':
        return 'light'
    elif user_theme == 'Dark Icons':
        return 'dark'
    elif user_theme == 'light' or user_theme == 'dark':
        return user_theme
    
    # Auto-Detection
    if user_theme == 'auto' or user_theme.startswith('Auto'):
        alfred_bg = os.getenv('alfred_theme_background', '')
        # rgba(34,32,44,1.00) = dunkler Hintergrund = light icons
        if alfred_bg and alfred_bg.startswith('rgba('):
            try:
                rgb_str = alfred_bg[5:-1]
                rgb_parts = rgb_str.split(',')
                
                if len(rgb_parts) >= 3:
                    r = float(rgb_parts[0])
                    g = float(rgb_parts[1])
                    b = float(rgb_parts[2])
                    
                    brightness = (r + g + b) / 3
                    # Dunkler Hintergrund (<128) = helle Icons
                    return 'light' if brightness < 128 else 'dark'
            except:
                pass
    
    return 'dark'

def update_workflow_icon():
    theme = get_icon_theme()
    
    # Pfade
    workflow_dir = os.path.dirname(os.path.abspath(__file__))
    theme_icon = os.path.join(workflow_dir, f"icons/{theme}/icon.png")
    workflow_icon = os.path.join(workflow_dir, "icon.png")
    
    # Kopiere das theme-spezifische Icon
    if os.path.exists(theme_icon):
        shutil.copy2(theme_icon, workflow_icon)
        print(f"Updated workflow icon to {theme} theme")

# If this file is executed directly, from Main Menu to update the workflow icon:
if __name__ == "__main__":
    update_workflow_icon()