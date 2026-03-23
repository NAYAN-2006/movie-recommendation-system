export default function SkeletonMovieCard() {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-zinc-900/60 shadow-lg shadow-black/50">
      <div className="aspect-[2/3] w-full animate-pulse bg-zinc-800" />
      <div className="absolute inset-0 flex flex-col justify-between p-4">
        <div className="flex justify-between">
          <div className="h-6 w-16 rounded-full bg-zinc-700" />
          <div className="h-6 w-12 rounded-full bg-zinc-700" />
        </div>
        <div className="space-y-2">
          <div className="h-4 w-3/4 rounded-full bg-zinc-700" />
          <div className="h-4 w-1/2 rounded-full bg-zinc-700" />
          <div className="h-8 w-full rounded-full bg-zinc-700" />
        </div>
      </div>
    </div>
  );
}
