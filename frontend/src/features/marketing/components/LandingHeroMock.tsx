/**
 * Stylised product mock — no screenshots or internal data.
 */
export function LandingHeroMock() {
  return (
    <div
      className="relative w-full max-w-lg mx-auto lg:mx-0"
      role="img"
      aria-label="EventLead branded form builder interface — illustrative mock"
    >
      <div className="rounded-xl border border-slate-200 bg-white shadow-lg overflow-hidden">
        <div className="flex items-center gap-2 px-4 py-3 bg-slate-50 border-b border-slate-200">
          <span className="h-2.5 w-2.5 rounded-full bg-red-400" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-400" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" aria-hidden="true" />
          <span className="ml-2 text-xs text-slate-500 font-medium">Form builder</span>
        </div>
        <div className="p-4 space-y-3 bg-gradient-to-br from-teal-50 to-white min-h-[220px]">
          <div className="rounded-lg bg-white/90 border border-teal-100 p-3 shadow-sm">
            <p className="text-xs font-semibold text-teal-800 mb-2">Event lead capture</p>
            <div className="space-y-2">
              <div className="h-2 w-full rounded bg-slate-100" />
              <div className="h-2 w-4/5 rounded bg-slate-100" />
              <div className="h-8 w-24 rounded-md bg-teal-600/80" />
            </div>
          </div>
          <div className="flex gap-2">
            <div className="flex-1 rounded-md border border-dashed border-slate-200 p-2 text-[10px] text-slate-400">
              Drag field
            </div>
            <div className="flex-1 rounded-md border border-slate-200 p-2 text-[10px] text-slate-600 bg-slate-50">
              Approval: pending
            </div>
          </div>
        </div>
      </div>
      <p className="sr-only">
        Illustrative mock of EventLead branded form builder interface and approval workflow
      </p>
    </div>
  )
}
