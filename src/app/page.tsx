// import Moon1 from './icons/moon_1.svg'

export default function RectanglePage() {
  return (
    <div className="relative flex items-center justify-center w-screen h-screen bg-[#0B131E] rounded-[50px] overflow-hidden">
      <div className="grid grid-flow-col grid-rows-3 grid-cols-3 gap-8">
        <div className="col-start-1">
          <div className="absolute top-12 left-12 w-[150px] h-[800px] bg-[#202B3B] rounded-[50px]"></div>
        </div>
        <div className="col-start-2">
          <div className="absolute top-12 left-64 w-[900px] h-[50px] bg-[#202B3B] rounded-[50px]"></div>
          <div className="absolute top-32 left-64 w-[900px] h-[350px] bg-[#000000] rounded-[50px]">
            <p className="text-white absolute top-12 left-12 font-bold text-7xl">Pearland</p>
            <p className="text-white absolute top-36 left-12 font-semibold text-5xl">110°</p>
            {/* <Moon1 priority src="/icons/moon_1.svg"></Moon1> */}
          </div>
          <div className="absolute bottom-20 left-64 w-[900px] h-[345px] bg-[#202B3B] rounded-[50px]"></div>
        </div>
        <div className="col-start-3">
          <div className="absolute top-12 right-12 w-[650px] h-[300px] bg-[#202B3B] rounded-[50px]"></div>
          <div className="absolute bottom-20 right-12 w-[650px] h-[475px] bg-[#202B3B] rounded-[50px]"></div>
        </div>
      </div>
    </div>
  );
}
