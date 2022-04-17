module.exports = {
    mode: "jit",
    purge: ["../views/*.html"],
    content: [],
    theme: {
        extend: {
            screens: {
                sm: '480px',
                md: '768px',
                lg: '976px',
                xl: '1440px',
            },
            colors: {
                "blue": "#1DA1F2",
                "darkblue": "#2795D9",
                "lightblue": "#EFF9FF",
                "dark": "#657786",
                "light": "#AAB8C2",
                "lighter": "#E1E8ED",
                "lightest": "#F5F8FA",
            },
            fontFamily: {
                sans: ['Helvetica Neue', 'sans-serif', 'Arial'],
                serif: ['Merriweather', 'serif'],
            },
            fontSize: {
                tiny:['8px', {
                    lineHeight: '0.5rem',
                }],
            },
        },
    },
    plugins: [],
}
