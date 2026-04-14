module matmul (
    input start,
    input signed [127:0] A,
    input signed [127:0] B,
    output reg signed [31:0] C0,
    output reg signed [31:0] C1,
    output reg signed [31:0] C2,
    output reg signed [31:0] C3
);

function signed [7:0] get_val;
    input [127:0] vec;
    input integer idx;
    begin
        get_val = vec[idx*8 +: 8];
    end
endfunction

always @(*) begin
    C0 = 0;
    C1 = 0;
    C2 = 0;
    C3 = 0;

    if (start) begin
        C0 = $signed(get_val(A,0)) * $signed(get_val(B,0))  +
             $signed(get_val(A,1)) * $signed(get_val(B,4))  +
             $signed(get_val(A,2)) * $signed(get_val(B,8))  +
             $signed(get_val(A,3)) * $signed(get_val(B,12));

        C1 = $signed(get_val(A,0)) * $signed(get_val(B,1))  +
             $signed(get_val(A,1)) * $signed(get_val(B,5))  +
             $signed(get_val(A,2)) * $signed(get_val(B,9))  +
             $signed(get_val(A,3)) * $signed(get_val(B,13));

        C2 = $signed(get_val(A,0)) * $signed(get_val(B,2))  +
             $signed(get_val(A,1)) * $signed(get_val(B,6))  +
             $signed(get_val(A,2)) * $signed(get_val(B,10)) +
             $signed(get_val(A,3)) * $signed(get_val(B,14));

        C3 = $signed(get_val(A,0)) * $signed(get_val(B,3))  +
             $signed(get_val(A,1)) * $signed(get_val(B,7))  +
             $signed(get_val(A,2)) * $signed(get_val(B,11)) +
             $signed(get_val(A,3)) * $signed(get_val(B,15));
    end
end

endmodule
