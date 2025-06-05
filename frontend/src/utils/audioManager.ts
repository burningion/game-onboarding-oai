// Global audio manager to ensure only one audio plays at a time
class AudioManager {
  private currentAudio: HTMLAudioElement | null = null;
  private currentUrl: string | null = null;

  async playAudio(url: string): Promise<HTMLAudioElement> {
    // Stop any currently playing audio
    this.stopCurrent();

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch audio: ${response.status}`);
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      this.currentAudio = audio;
      this.currentUrl = audioUrl;

      // Clean up when audio ends
      audio.onended = () => {
        if (this.currentUrl) {
          URL.revokeObjectURL(this.currentUrl);
        }
        this.currentAudio = null;
        this.currentUrl = null;
      };

      // Handle errors
      audio.onerror = () => {
        console.error('Audio playback error');
        if (this.currentUrl) {
          URL.revokeObjectURL(this.currentUrl);
        }
        this.currentAudio = null;
        this.currentUrl = null;
      };

      // Start playback
      await audio.play();
      return audio;

    } catch (error) {
      console.error('Error playing audio:', error);
      throw error;
    }
  }

  stopCurrent() {
    if (this.currentAudio) {
      this.currentAudio.pause();
      this.currentAudio.currentTime = 0;
      
      if (this.currentUrl) {
        URL.revokeObjectURL(this.currentUrl);
      }
      
      this.currentAudio = null;
      this.currentUrl = null;
    }
  }

  isPlaying(): boolean {
    return this.currentAudio !== null && !this.currentAudio.paused;
  }
}

// Export singleton instance
export const audioManager = new AudioManager();