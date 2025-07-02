from dataclasses import dataclass
from typing import  Generator
from tripio.result import Result, Ok, Err, is_ok, is_err

@dataclass
class OutRecord:
    last_count: int
    tokens_requested: int
    accumulate: int
    leak_count: int

class DummyDevice:
    def __init__(self):
        ...
    #實際執行的生成器方法, return 應該被考慮
    def _out(self, i:int) -> Generator[Result[OutRecord,Exception],Err[Exception] , None]:
        for i in range(i):
            result: Result[OutRecord, Exception] = Ok(OutRecord(i, i, i, i)).wrap()
            
            #
            if i == 3:
                result= Err(Exception("Simulated error on count 3")).wrap()
                
            recvd = yield result
            if recvd:
                print(recvd.unwrap())
    #這種包裝應該要被簡化
    def out(self,i:int):
        self.g = self._out(i)
        return self.g
    #尚未測試從外部觸發的錯誤
    def next_wrong(self):
        self.g.send(Err(Exception("Something went wrong!")))

def main():
    dd = DummyDevice()
    #假設發送5枚, 應該要收到5枚確認
    for r in dd.out(5):
        #有點太繁瑣
        if is_ok(r):#正常流程
            ok = r.unwrap()
            print(ok)
        elif is_err(r):#錯誤處理流程
            try:
                #明確表示是錯誤處理, 但還是太多分支了
                r.unwrap()
            except Exception as e:
                print(f"Exception occurred: {e}")
                break#可break 或 continue或不處理
    else:
        print("All operations completed successfully.")
        
if __name__ == "__main__":
    main()