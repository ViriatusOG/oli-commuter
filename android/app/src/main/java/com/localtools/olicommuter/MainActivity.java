package com.localtools.olicommuter;

import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.WebSettings;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    // The board is designed for one column: keep it portrait, always.
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        // Honour the phone's Font size setting — the WebView ignores it by default.
        try {
            float fontScale = getResources().getConfiguration().fontScale;
            int zoom = Math.round(fontScale * 100f);
            zoom = Math.max(80, Math.min(zoom, 200));
            if (zoom != 100) {
                WebSettings ws = getBridge().getWebView().getSettings();
                ws.setTextZoom(zoom);
            }
        } catch (Exception ignore) { }

        // No white flash before the page paints on a dark-mode phone.
        boolean night = (getResources().getConfiguration().uiMode
                & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;
        int bg = night ? Color.parseColor("#0d0c12") : Color.parseColor("#f3f2f7");
        getWindow().getDecorView().setBackgroundColor(bg);
        try { getBridge().getWebView().setBackgroundColor(bg); } catch (Exception ignore) { }
    }
}
