export interface OliUpdaterDownloadResult { path: string; sha256: string; }
export interface OliUpdater {
  download(options: { url: string; sha256?: string }): Promise<OliUpdaterDownloadResult>;
  install(options: { path: string }): Promise<void>;
  addListener(event: "progress", listener: (ev: { pct: number }) => void): Promise<{ remove: () => void }>;
}
