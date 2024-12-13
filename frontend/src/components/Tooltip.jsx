export default function Tooltip({ message, direction, children, classNames }) {
    const directionClasses = {
        top: 'bottom-6',
        right: 'left-8 -top-2',
        bottom: 'top-6',
        left: 'right-8 -top-2'
    };
    return (
        <div className={`group relative flex flex-col items-center ${classNames}`}>
            {children}
            <span className={`absolute ${directionClasses[direction]} scale-0 transition-all rounded bg-gray-800 p-2 text-xs text-white group-hover:scale-100 z-50`}>{message}</span>
        </div>
    )
}