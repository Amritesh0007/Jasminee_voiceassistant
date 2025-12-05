"""
Patch script to fix torchaudio compatibility issue with speechbrain
"""
import torchaudio
from typing import List

def patch_torchaudio():
    """Add missing list_audio_backends function to torchaudio"""
    if not hasattr(torchaudio, 'list_audio_backends'):
        def list_audio_backends() -> List[str]:
            """
            Dummy implementation of list_audio_backends for compatibility
            Returns a list of common audio backends
            """
            # Return common backends that are typically available
            return ['soundfile', 'sox_io']
        
        # Add the function to torchaudio using setattr to avoid type checking issues
        setattr(torchaudio, 'list_audio_backends', list_audio_backends)
        print("✓ Patched torchaudio with list_audio_backends function")
        return True
    else:
        print("✓ torchaudio.list_audio_backends already exists")
        return False

if __name__ == "__main__":
    patch_torchaudio()