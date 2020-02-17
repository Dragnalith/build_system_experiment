void POST_PROCESS_VS(in in_vertex, out out_vertex) {
    vec4 offset(0, 0, 1, 0);
    out_vertex = in_vertex + offset;
}