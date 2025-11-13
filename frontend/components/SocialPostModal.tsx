import { useState } from 'react';

interface SocialPostModalProps {
  caption: string;
  imageUrl?: string;
  onClose: () => void;
}

export default function SocialPostModal({ caption, imageUrl, onClose }: SocialPostModalProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyCaption = async () => {
    try {
      await navigator.clipboard.writeText(caption);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-2xl font-bold text-gray-900">Social Media Post</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Image */}
          {imageUrl ? (
            <div className="w-full mb-6 rounded-lg overflow-hidden bg-gray-200">
              <img
                src={imageUrl}
                alt="Social post image"
                className="w-full h-auto max-h-96 object-contain rounded-lg"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  const parent = target.parentElement;
                  if (parent) {
                    parent.innerHTML = '<div class="w-full h-64 flex items-center justify-center bg-gray-100 rounded-lg"><p class="text-gray-500">Image failed to load</p></div>';
                  }
                }}
                onLoad={() => {
                  console.log('✅ Image loaded successfully:', imageUrl);
                }}
              />
            </div>
          ) : (
            <div className="w-full mb-6 rounded-lg overflow-hidden bg-gray-100 h-64 flex items-center justify-center">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mb-2"></div>
                <p className="text-gray-600 text-sm">Generating image with DALL·E...</p>
                <p className="text-gray-500 text-xs mt-1">This may take 10-20 seconds</p>
              </div>
            </div>
          )}

          {/* Caption */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <label className="text-sm font-semibold text-gray-700">Caption</label>
              <button
                onClick={handleCopyCaption}
                className="px-3 py-1 bg-primary-600 text-white rounded text-sm hover:bg-primary-700 transition-colors"
              >
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
              <p className="text-gray-800 whitespace-pre-wrap">{caption}</p>
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Tip:</strong> Copy the caption and use it with the generated image for your social media posts.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end gap-4 p-6 border-t">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

