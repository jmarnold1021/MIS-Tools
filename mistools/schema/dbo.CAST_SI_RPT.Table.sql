DROP TABLE [dbo].[CAST_SI_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_SI_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_SI_RPT](
	[CAST_SI_RPT_ID] [int] NOT NULL,
	[CAST_SI_RPT_FLAG] [bit] NOT NULL,
	[CAST_SI_WORK_ID] [varchar](10) NULL,
	[CASTSI_GI01] [varchar](3) NULL,
	[CASTSI_SB00_OLD] [varchar](9) NULL,
	[CASTSI_SB01_OLD] [varchar](1) NULL,
	[CASTSI_SB00_NEW] [varchar](9) NULL,
	[CASTSI_SG01_NEW] [varchar](1) NULL,
 CONSTRAINT [PK_SI_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_SI_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_SI_R__CAST___0462B21D]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_SI_RPT] ADD  DEFAULT ((1)) FOR [CAST_SI_RPT_FLAG]
END
GO
