// ============================================================
// 3D Tilt Effect — Mouse-tracked card tilt
// ============================================================

export function applyTilt(element: HTMLElement, intensity = 15): () => void {
  const onMove = (e: MouseEvent) => {
    const rect = element.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    const rotateX = ((y - centerY) / centerY) * -intensity
    const rotateY = ((x - centerX) / centerX) * intensity

    element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.03, 1.03, 1.03)`
    element.style.transition = 'transform 0.1s ease'

    // Dynamic shine
    const shine = element.querySelector('.tilt-shine') as HTMLElement
    if (shine) {
      shine.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.12) 0%, transparent 60%)`
    }
  }

  const onLeave = () => {
    element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
    element.style.transition = 'transform 0.5s ease'
    const shine = element.querySelector('.tilt-shine') as HTMLElement
    if (shine) shine.style.background = 'transparent'
  }

  // Add shine layer
  const shine = document.createElement('div')
  shine.className = 'tilt-shine'
  shine.style.cssText = 'position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:1;transition:background 0.1s;'
  element.style.position = 'relative'
  element.appendChild(shine)

  element.addEventListener('mousemove', onMove)
  element.addEventListener('mouseleave', onLeave)

  return () => {
    element.removeEventListener('mousemove', onMove)
    element.removeEventListener('mouseleave', onLeave)
  }
}
