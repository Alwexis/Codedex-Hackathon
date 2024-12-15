export default function ConfirmModal({ isOpen, onClose, onConfirm, message }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/75 flex items-center justify-center p-4 z-50">
            <div className="bg-white border-2 border-black p-6 w-full max-w-sm shadow-[4px_4px_0_0_rgba(0,0,0,1)]">
                <p className="text-lg font-bold mb-4">{message}</p>
                <div className="flex justify-end space-x-2">
                    <button
                        onClick={onClose}
                        className="cursor-pointer px-4 py-2 bg-gray-500 text-white font-bold border-2 border-black hover:bg-gray-600 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={() => {
                            onConfirm();
                            onClose();
                        }}
                        className="cursor-pointer px-4 py-2 bg-red-500 text-white font-bold border-2 border-black hover:bg-red-600 transition-colors"
                    >
                        Delete
                    </button>
                </div>
            </div>
        </div>
    );
}
