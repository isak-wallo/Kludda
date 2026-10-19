package com.keiws.kludda;

import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;
import androidx.activity.OnBackPressedCallback;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

// Kludda som app: helskärm (systemfälten dolda, de glider fram en stund vid
// svep från kanten), bakåt gör ingenting och vridningen är låst i
// AndroidManifest.xml (sensorLandscape).
public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Bakåtknappen och bakåtsvepet: ingenting, så att barnet inte råkar
        // lämna appen. Hem-knappen fungerar som vanligt.
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {}
        });
        // Rita ända ut, också bakom en kameraurgröpning.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            getWindow().getAttributes().layoutInDisplayCutoutMode =
                WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
        }
        doljSystemfalten();
    }

    // Fälten döljs igen varje gång appen får tillbaka fokus (efter
    // appväxlaren, skärmlåset eller ett svep).
    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) doljSystemfalten();
    }

    private void doljSystemfalten() {
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }
}
