package com.localtools.olicommuter.update;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import android.content.pm.PackageManager;

import androidx.core.content.FileProvider;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.MessageDigest;

/**
 * The in-app update path for Oli Commuter:
 *
 *  - download(url, sha256)  fetches an APK straight to the phone's cache,
 *    streaming, with progress events, and refuses to keep a file whose
 *    SHA-256 does not match what the release published
 *  - install(path)          hands the file to Android's package installer
 *
 * It is intentionally a dumb pair of methods: the version comparison, the
 * "is this worth offering?" decision and all the user-facing text live in
 * the web app, where the rest of the app lives.
 */
@CapacitorPlugin(name = "OliUpdater")
public class OliUpdaterPlugin extends Plugin {

    public static final String MIME_APK = "application/vnd.android.package-archive";
    public static final String EVENT_PROGRESS = "progress";
    /* the app manifest already registers a FileProvider over the cache dir */
    private String authority() { return getContext().getPackageName() + ".fileprovider"; }

    private File target() {
        File dir = new File(getContext().getCacheDir(), "oli-updates");
        if (!dir.exists() && !dir.mkdirs()) throw new IllegalStateException("cannot create " + dir);
        return new File(dir, "oli-update.apk");
    }

    @PluginMethod
    public void download(PluginCall call) {
        String urlStr = call.getString("url");
        String expected = call.getString("sha256");
        if (urlStr == null || urlStr.isEmpty()) { call.reject("Missing url"); return; }
        execute(() -> {
            File out = target();
            HttpURLConnection conn = null;
            try {
                conn = (HttpURLConnection) new URL(urlStr).openConnection();
                conn.setConnectTimeout(15000);
                conn.setReadTimeout(30000);
                conn.setRequestProperty("User-Agent", "Oli-Commuter-in-app-update");
                int code = conn.getResponseCode();
                if (code != 200) { call.reject("Download failed: HTTP " + code); return; }
                long total = conn.getContentLengthLong();
                long done = 0;
                int lastPct = -1;
                try (InputStream in = conn.getInputStream(); FileOutputStream fos = new FileOutputStream(out)) {
                    byte[] buf = new byte[16384];
                    int n;
                    while ((n = in.read(buf)) != -1) {
                        fos.write(buf, 0, n);
                        done += n;
                        if (total > 0) {
                            int pct = (int) (done * 100 / total);
                            if (pct > lastPct) { lastPct = pct; sendProgress(pct); }
                        }
                    }
                }
                String actual = sha256Hex(out);
                if (expected != null && !expected.trim().isEmpty() && !expected.trim().equalsIgnoreCase(actual)) {
                    out.delete();
                    call.reject("The download failed its checksum check, so it was deleted. Try again later.");
                    return;
                }
                sendProgress(100);
                call.resolve(new JSObject().put("path", out.getAbsolutePath()).put("sha256", actual).put("bytes", done));
            } catch (Exception e) {
                if (out.exists()) out.delete();
                call.reject("Download failed: " + e.getMessage(), e);
            } finally {
                if (conn != null) conn.disconnect();
            }
        });
    }

    @PluginMethod
    public void sha256(PluginCall call) {
        String path = call.getString("path");
        File f = new File(path == null ? "" : path);
        if (!f.exists()) { call.reject("No file at " + path); return; }
        try {
            call.resolve(new JSObject().put("sha256", sha256Hex(f)));
        } catch (Exception e) {
            call.reject("Could not read the file: " + e.getMessage(), e);
        }
    }

    @PluginMethod
    public void install(PluginCall call) {
        String path = call.getString("path");
        File f = new File(path == null ? "" : path);
        if (!f.exists()) { call.reject("There is no downloaded update to install."); return; }
        /* Android 11+ only lets an app hand over an APK once the user has
           granted it "install unknown apps".  If that switch is off, open the
           exact system page for this app instead of failing silently. */
        if (Build.VERSION.SDK_INT >= 26 &&
            !getContext().getPackageManager().canRequestPackageInstalls()) {
            try {
                Intent perm = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                        Uri.parse("package:" + getContext().getPackageName()));
                perm.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(perm);
                JSObject ret = new JSObject().put("needsPermission", true);
                call.resolve(ret);
                return;
            } catch (Exception ignore) { /* fall through to the normal intent */ }
        }
        try {
            Uri uri = FileProvider.getUriForFile(getContext(), authority(), f);
            Intent intent = new Intent(Build.VERSION.SDK_INT >= 30 ? Intent.ACTION_INSTALL_PACKAGE : Intent.ACTION_VIEW);
            intent.setDataAndType(uri, MIME_APK);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(intent);
            call.resolve(new JSObject().put("needsPermission", false));
        } catch (Exception e) {
            call.reject("Could not start the installer: " + e.getMessage(), e);
        }
    }

    private void sendProgress(int pct) {
        notifyListeners(EVENT_PROGRESS, new JSObject().put("pct", pct));
    }

    private String sha256Hex(File f) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        try (InputStream in = new FileInputStream(f)) {
            byte[] buf = new byte[65536];
            int n;
            while ((n = in.read(buf)) != -1) md.update(buf, 0, n);
        }
        byte[] d = md.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b : d) sb.append(String.format("%02x", b));
        return sb.toString();
    }
}
